#include "APresa.h"
#include "AEntorno.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

TArray<FIntPoint> APresa::DirOffsets = {
    FIntPoint(-1,  0), // UP
    FIntPoint( 1,  0), // DOWN
    FIntPoint( 0, -1), // LEFT
    FIntPoint( 0,  1), // RIGHT
    FIntPoint( 0,  0)  // STAY
};



static int32 DirectionTo(const FIntPoint& Src, const FIntPoint& Dst)
{
    const int32 Dx = Dst.X - Src.X;
    const int32 Dy = Dst.Y - Src.Y;
    if (Dx == 0 && Dy == 0)
    {
        return 0;
    }
    if (FMath::Abs(Dx) >= FMath::Abs(Dy))
    {
        return Dx < 0 ? 1 : 2; // UP / DOWN
    }
    return Dy < 0 ? 3 : 4; // LEFT / RIGHT
}

void NearestInfo(AEntorno* Entorno, const FIntPoint& Src, const TArray<FIntPoint>& Positions, int32& OutDist, int32& OutDir)
{
    OutDist = -1;
    OutDir = 0;
    for (const FIntPoint& Pos : Positions)
    {
        const int32 Dist = Entorno->Manhattan(Src, Pos);
        if (OutDist < 0 || Dist < OutDist)
        {
            OutDist = Dist;
            OutDir = DirectionTo(Src, Pos);
        }
    }
}


APresa::APresa()
{
    PrimaryActorTick.bCanEverTick = false;

    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComp;

    static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshAsset(TEXT("/Game/LevelPrototyping/Meshes/SM_ChamferCube.SM_ChamferCube"));
    if (MeshAsset.Succeeded())
    {
        MeshComp->SetStaticMesh(MeshAsset.Object);
    }
    MeshComp->SetWorldScale3D(FVector(0.8f));
    MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}

void APresa::BeginPlay()
{
    Super::BeginPlay();
    LoadQTable();
}

void APresa::LoadQTable()
{
    if (bQTableLoaded) return;

    FString FullPath;
    if (FPaths::IsRelative(QTableFilePath))
    {
        FullPath = FPaths::ProjectDir() + QTableFilePath;
    }
    else
    {
        FullPath = QTableFilePath;
    }

    FString JsonStr;
    if (!FFileHelper::LoadFileToString(JsonStr, *FullPath))
    {
        UE_LOG(LogTemp, Error, TEXT("[APresa] Failed to load Q-Table file: %s"), *FullPath);
        return;
    }

    TSharedPtr<FJsonObject> JsonObj;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonStr);
    if (!FJsonSerializer::Deserialize(Reader, JsonObj) || !JsonObj.IsValid())
    {
        UE_LOG(LogTemp, Error, TEXT("[APresa] Failed to parse Q-Table JSON"));
        return;
    }

    NumStates = JsonObj->GetIntegerField(TEXT("n_states"));
    NumActions = JsonObj->GetIntegerField(TEXT("n_actions"));

    const TArray<TSharedPtr<FJsonValue>>* QTableRaw;
    if (!JsonObj->TryGetArrayField(TEXT("q_table"), QTableRaw))
    {
        UE_LOG(LogTemp, Error, TEXT("[APresa] q_table field not found in JSON"));
        return;
    }

    QTable.SetNum(NumStates);
    for (int32 s = 0; s < NumStates && s < QTableRaw->Num(); s++)
    {
        const TArray<TSharedPtr<FJsonValue>>* Row;
        if ((*QTableRaw)[s]->TryGetArray(Row))
        {
            QTable[s].SetNum(NumActions);
            for (int32 a = 0; a < NumActions && a < Row->Num(); a++)
            {
                QTable[s][a] = (*Row)[a]->AsNumber();
            }
        }
    }

    bQTableLoaded = true;
    UE_LOG(LogTemp, Log, TEXT("[APresa] Q-Table loaded: %d states x %d actions from %s"),
           NumStates, NumActions, *FullPath);
}

int32 APresa::GetState(AEntorno* Entorno)
{
    TArray<FIntPoint> Recursos = Entorno->GetResourcePositions();
    TArray<FIntPoint> Preds = Entorno->GetPredatorPositions();

    int32 ResourceDist = -1;
    int32 rd = 0;
    NearestInfo(Entorno, GridPos, Recursos, ResourceDist, rd);

    int32 rs = 0;
    if (ResourceDist >= 0)
    {
        if (ResourceDist <= 1)
        {
            rs = 2;
        }
        else if (ResourceDist <= 5)
        {
            rs = 1;
        }
    }

    float Ratio = (float)Hambre / (float)MaxHambre;
    int32 hs = 0;
    if (Ratio <= 0.7f)
        hs = (Ratio > 0.3f) ? 1 : 2;

    int32 rr = 0;
    for (const FIntPoint& P : Entorno->GetPreyPositions())
    {
        if (P != GridPos && Entorno->Manhattan(GridPos, P) <= 2)
        {
            rr = 1;
            break;
        }
    }

    int32 PredatorDist = -1;
    int32 pd = 0;
    NearestInfo(Entorno, GridPos, Preds, PredatorDist, pd);

    int32 prs = 0;
    if (PredatorDist >= 0)
    {
        if (PredatorDist < 3)
        {
            prs = 2;
        }
        else if (PredatorDist <= 5)
        {
            prs = 1;
        }
    }

    return rs
        + rd * RS_LEVELS
        + hs * RS_LEVELS * RD_LEVELS
        + rr * RS_LEVELS * RD_LEVELS * HB_LEVELS
        + prs * RS_LEVELS * RD_LEVELS * HB_LEVELS * RR_LEVELS
        + pd * RS_LEVELS * RD_LEVELS * HB_LEVELS * RR_LEVELS * PR_LEVELS;
}

int32 APresa::ChooseAction(int32 StateIdx)
{
    if (!bQTableLoaded || !QTable.IsValidIndex(StateIdx))
    {
        return FMath::RandRange(0, NumActions - 1);
    }

    TArray<int32> BestActions;
    BestActions.Add(0);
    float BestValue = QTable[StateIdx][0];
    for (int32 a = 1; a < NumActions; a++)
    {
        if (QTable[StateIdx][a] > BestValue)
        {
            BestValue = QTable[StateIdx][a];
            BestActions.Reset();
            BestActions.Add(a);
        }
        else if (QTable[StateIdx][a] == BestValue)
        {
            BestActions.Add(a);
        }
    }
    return BestActions[FMath::RandRange(0, BestActions.Num() - 1)];
}

void APresa::ApplyAction(int32 ActionIdx, AEntorno* Entorno)
{
    if (!Entorno || !bAlive) return;

    FIntPoint NewPos = GridPos + DirOffsets[ActionIdx];

    if (Entorno->IsValidPos(NewPos))
    {
        EEntornoCellType Target = Entorno->GetCellType(NewPos);

        if (Target == EEntornoCellType::Empty)
        {
            Entorno->MovePrey(this, NewPos);
        }
        else if (Target == EEntornoCellType::Resource)
        {
            Entorno->MovePrey(this, NewPos);
            Entorno->RemoveResource(NewPos);
            Hambre = FMath::Min(MaxHambre, Hambre + 40);
        }
        else if (Target == EEntornoCellType::Predator)
        {
        }
    }

    Hambre = FMath::Max(0, Hambre - 1);
    if (Hambre <= 0)
    {
        StepsHambreCero++;
    }
    else
    {
        StepsHambreCero = 0;
    }

    if (ReproCooldown > 0)
    {
        ReproCooldown--;
    }

    if (StepsHambreCero >= 5)
    {
        bAlive = false;
        UE_LOG(LogTemp, Verbose, TEXT("[APresa] %s died of starvation"), *GetName());
    }
}
