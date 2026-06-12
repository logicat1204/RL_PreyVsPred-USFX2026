#include "AEntorno.h"
#include "APresa.h"
#include "APredator.h"
#include "ARecurso.h"
#include "Algo/Sort.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"

AEntorno::AEntorno()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AEntorno::BeginPlay()
{
    Super::BeginPlay();
    GridOrigin = GetActorLocation();
}

void AEntorno::InitializeSimulation()
{
    ResetSimulation();

    int32 Total = InitialPreyCount + InitialPredatorCount + MaxResources;
    TArray<FIntPoint> AllFree = GetFreeSpaces();

    UE_LOG(LogTemp, Log, TEXT("[Init] Free cells: %d | Need: %dP + %dD + %dR = %d"),
           AllFree.Num(), InitialPreyCount, InitialPredatorCount, MaxResources, Total);

    if (AllFree.Num() < Total)
    {
        UE_LOG(LogTemp, Warning, TEXT("[Init] Not enough free spaces"));
        return;
    }

    for (int32 i = AllFree.Num() - 1; i > 0; i--)
    {
        int32 j = FMath::RandRange(0, i);
        AllFree.Swap(i, j);
    }

    UE_LOG(LogTemp, Log, TEXT("[Init] PreyClass=%s  PredatorClass=%s"),
           PreyClass ? *PreyClass->GetName() : TEXT("NULL"),
           PredatorClass ? *PredatorClass->GetName() : TEXT("NULL"));

    if (!PreyClass)
    {
        UE_LOG(LogTemp, Error, TEXT("[Init] PreyClass not set in AEntorno"));
        return;
    }
    if (!PredatorClass)
    {
        UE_LOG(LogTemp, Error, TEXT("[Init] PredatorClass not set in AEntorno"));
        return;
    }

    UWorld* World = GetWorld();
    if (!World)
    {
        UE_LOG(LogTemp, Error, TEXT("[Init] No World"));
        return;
    }

    // Spawn preys
    UE_LOG(LogTemp, Log, TEXT("[Init] Spawning %d preys..."), InitialPreyCount);
    for (int32 i = 0; i < InitialPreyCount; i++)
    {
        FVector Location = GridToWorld(AllFree[i]);
        FRotator Rotation = FRotator::ZeroRotator;

        APresa* Prey = World->SpawnActor<APresa>(PreyClass, Location, Rotation);
        if (Prey)
        {
            Prey->GridPos = AllFree[i];
            Prey->Hambre = 100;
            Prey->MaxHambre = 100;
            Prey->bAlive = true;
            Prey->ReproCooldown = 0;
            Prey->StepsHambreCero = 0;
            Preys.Add(Prey);
            UE_LOG(LogTemp, Verbose, TEXT("[Init] Spawned prey at (%d,%d)"), AllFree[i].X, AllFree[i].Y);
        }
        else
        {
            UE_LOG(LogTemp, Error, TEXT("[Init] Failed to spawn prey %d"), i);
        }
    }

    // Spawn predators
    int32 Offset = InitialPreyCount;
    UE_LOG(LogTemp, Log, TEXT("[Init] Spawning %d predators..."), InitialPredatorCount);
    for (int32 i = 0; i < InitialPredatorCount; i++)
    {
        FVector Location = GridToWorld(AllFree[Offset + i]);
        FRotator Rotation = FRotator::ZeroRotator;

        APredator* Pred = World->SpawnActor<APredator>(PredatorClass, Location, Rotation);
        if (Pred)
        {
            Pred->GridPos = AllFree[Offset + i];
            Pred->Hambre = 100;
            Pred->MaxHambre = 100;
            Pred->bAlive = true;
            Pred->ReproCooldown = 0;
            Pred->StepsHambreCero = 0;
            Predators.Add(Pred);
            UE_LOG(LogTemp, Verbose, TEXT("[Init] Spawned predator at (%d,%d)"), AllFree[Offset + i].X, AllFree[Offset + i].Y);
        }
        else
        {
            UE_LOG(LogTemp, Error, TEXT("[Init] Failed to spawn predator %d"), i);
        }
    }

    // Spawn resources
    Offset += InitialPredatorCount;
    ResourcePositions.Reset();
    ResourceMeshes.Reset();
    for (int32 i = 0; i < MaxResources && (Offset + i) < AllFree.Num(); i++)
    {
        FIntPoint RPos = AllFree[Offset + i];
        ResourcePositions.Add(RPos);

        ARecurso* Res = World->SpawnActor<ARecurso>(GridToWorld(RPos), FRotator(10.0f, 0.0f, 60.0f));
        if (Res)
        {
            Res->GridPos = RPos;
            ResourceMeshes.Add(Res);
        }
    }

    UE_LOG(LogTemp, Log, TEXT("[Init] COMPLETE: %d preys, %d predators, %d resources at %d,%d"),
           Preys.Num(), Predators.Num(), ResourcePositions.Num(), GridSizeX, GridSizeY);
}

void AEntorno::ResetSimulation()
{
    UWorld* World = GetWorld();
    if (World)
    {
        for (auto* P : Preys)
        {
            if (P) World->DestroyActor(P);
        }
        for (auto* D : Predators)
        {
            if (D) World->DestroyActor(D);
        }
        for (auto* R : ResourceMeshes)
        {
            if (R) World->DestroyActor(R);
        }
    }
    Preys.Empty();
    Predators.Empty();
    ResourcePositions.Empty();
    ResourceMeshes.Empty();
    TotalPreyReproductions = 0;
    TotalPredatorReproductions = 0;
}

void AEntorno::Step()
{
    // Preys act first
    TArray<APresa*> AlivePreys;
    for (auto* P : Preys)
    {
        if (P && P->bAlive) AlivePreys.Add(P);
    }

    if (AlivePreys.Num() == 0 && Predators.Num() == 0)
    {
        return;
    }

    // Shuffle (randomize order)
    for (int32 i = AlivePreys.Num() - 1; i > 0; i--)
    {
        int32 j = FMath::RandRange(0, i);
        AlivePreys.Swap(i, j);
    }

    for (auto* P : AlivePreys)
    {
        if (P->bAlive)
        {
            int32 State = P->GetState(this);
            int32 Action = P->ChooseAction(State);
            FIntPoint OldPos = P->GridPos;
            P->ApplyAction(Action, this);
            if (P->GridPos != OldPos)
            {
                UE_LOG(LogTemp, Verbose, TEXT("[Step] %s moved (%d,%d)->(%d,%d)"),
                       *P->GetName(), OldPos.X, OldPos.Y, P->GridPos.X, P->GridPos.Y);
            }
        }
    }

    // Predators act
    TArray<APredator*> AlivePreds;
    for (auto* D : Predators)
    {
        if (D && D->bAlive) AlivePreds.Add(D);
    }

    for (int32 i = AlivePreds.Num() - 1; i > 0; i--)
    {
        int32 j = FMath::RandRange(0, i);
        AlivePreds.Swap(i, j);
    }

    for (auto* D : AlivePreds)
    {
        if (D->bAlive)
        {
            int32 State = D->GetState(this);
            int32 Action = D->ChooseAction(State);
            FIntPoint OldPos = D->GridPos;
            D->ApplyAction(Action, this);
            if (D->GridPos != OldPos)
            {
                UE_LOG(LogTemp, Verbose, TEXT("[Step] %s moved (%d,%d)->(%d,%d)"),
                       *D->GetName(), OldPos.X, OldPos.Y, D->GridPos.X, D->GridPos.Y);
            }
        }
    }

    CleanupDeadAgents();
    HandleReproduction();
    CleanupDeadAgents();

    // Spawn resources randomly
    if (FMath::RandRange(0, 100) < 30 && ResourcePositions.Num() < MaxResources)
    {
        SpawnResource();
    }
}

bool AEntorno::IsValidPos(const FIntPoint& Pos) const
{
    return Pos.X >= 0 && Pos.X < GridSizeX && Pos.Y >= 0 && Pos.Y < GridSizeY;
}

bool AEntorno::IsFree(const FIntPoint& Pos) const
{
    if (!IsValidPos(Pos)) return false;
    return !IsPreyAt(Pos) && !IsPredatorAt(Pos);
}

EEntornoCellType AEntorno::GetCellType(const FIntPoint& Pos) const
{
    if (!IsValidPos(Pos)) return EEntornoCellType::Invalid;
    if (IsPreyAt(Pos)) return EEntornoCellType::Prey;
    if (IsPredatorAt(Pos)) return EEntornoCellType::Predator;
    if (IsResourceAt(Pos)) return EEntornoCellType::Resource;
    return EEntornoCellType::Empty;
}

FVector AEntorno::GridToWorld(const FIntPoint& Pos) const
{
    return GridOrigin + FVector(Pos.X * CellSize, Pos.Y * CellSize, 0.0f);
}

int32 AEntorno::Manhattan(const FIntPoint& A, const FIntPoint& B) const
{
    return FMath::Abs(A.X - B.X) + FMath::Abs(A.Y - B.Y);
}

TArray<FIntPoint> AEntorno::GetFreeSpaces() const
{
    TArray<FIntPoint> Free;
    for (int32 x = 0; x < GridSizeX; x++)
    {
        for (int32 y = 0; y < GridSizeY; y++)
        {
            FIntPoint Pos(x, y);
            if (IsFree(Pos)) Free.Add(Pos);
        }
    }
    return Free;
}

TArray<FIntPoint> AEntorno::GetPreyPositions() const
{
    TArray<FIntPoint> Result;
    for (auto* P : Preys)
    {
        if (P && P->bAlive) Result.Add(P->GridPos);
    }
    return Result;
}

TArray<FIntPoint> AEntorno::GetPredatorPositions() const
{
    TArray<FIntPoint> Result;
    for (auto* D : Predators)
    {
        if (D && D->bAlive) Result.Add(D->GridPos);
    }
    return Result;
}

TArray<FIntPoint> AEntorno::GetResourcePositions() const
{
    return ResourcePositions;
}

void AEntorno::MovePrey(APresa* Prey, const FIntPoint& NewPos)
{
    if (Prey && IsValidPos(NewPos))
    {
        Prey->GridPos = NewPos;
    }
}

void AEntorno::MovePredator(APredator* Pred, const FIntPoint& NewPos)
{
    if (Pred && IsValidPos(NewPos))
    {
        Pred->GridPos = NewPos;
    }
}

APresa* AEntorno::GetPreyAt(const FIntPoint& Pos)
{
    for (auto* P : Preys)
    {
        if (P && P->bAlive && P->GridPos == Pos) return P;
    }
    return nullptr;
}

APredator* AEntorno::GetPredatorAt(const FIntPoint& Pos)
{
    for (auto* D : Predators)
    {
        if (D && D->bAlive && D->GridPos == Pos) return D;
    }
    return nullptr;
}

void AEntorno::SpawnResource()
{
    TArray<FIntPoint> Free = GetFreeSpaces();
    if (Free.Num() > 0)
    {
        int32 Idx = FMath::RandRange(0, Free.Num() - 1);
        FIntPoint RPos = Free[Idx];
        ResourcePositions.Add(RPos);

        UWorld* World = GetWorld();
        if (World)
        {
            ARecurso* Res = World->SpawnActor<ARecurso>(GridToWorld(RPos), FRotator(10.0f, 0.0f, 60.0f));
            if (Res)
            {
                Res->GridPos = RPos;
                ResourceMeshes.Add(Res);
            }
        }
    }
}

void AEntorno::RemoveResource(const FIntPoint& Pos)
{
    ResourcePositions.Remove(Pos);

    for (int32 i = ResourceMeshes.Num() - 1; i >= 0; i--)
    {
        if (ResourceMeshes[i] && ResourceMeshes[i]->GridPos == Pos)
        {
            UWorld* World = GetWorld();
            if (World) World->DestroyActor(ResourceMeshes[i]);
            ResourceMeshes.RemoveAt(i);
            break;
        }
    }
}

bool AEntorno::IsPreyAt(const FIntPoint& Pos) const
{
    for (auto* P : Preys)
    {
        if (P && P->bAlive && P->GridPos == Pos) return true;
    }
    return false;
}

bool AEntorno::IsPredatorAt(const FIntPoint& Pos) const
{
    for (auto* D : Predators)
    {
        if (D && D->bAlive && D->GridPos == Pos) return true;
    }
    return false;
}

bool AEntorno::IsResourceAt(const FIntPoint& Pos) const
{
    return ResourcePositions.Contains(Pos);
}

void AEntorno::CleanupDeadAgents()
{
    UWorld* World = GetWorld();

    for (int32 i = Preys.Num() - 1; i >= 0; i--)
    {
        if (Preys[i] && !Preys[i]->bAlive)
        {
            UE_LOG(LogTemp, Verbose, TEXT("[Step] %s died"), *Preys[i]->GetName());
            if (World)
            {
                World->DestroyActor(Preys[i]);
            }
            Preys.RemoveAt(i);
        }
    }

    for (int32 i = Predators.Num() - 1; i >= 0; i--)
    {
        if (Predators[i] && !Predators[i]->bAlive)
        {
            UE_LOG(LogTemp, Verbose, TEXT("[Step] %s died"), *Predators[i]->GetName());
            if (World)
            {
                World->DestroyActor(Predators[i]);
            }
            Predators.RemoveAt(i);
        }
    }
}

void AEntorno::HandleReproduction()
{
    TArray<APresa*> PreySnapshot = Preys;
    for (APresa* P : PreySnapshot)
    {
        if (Preys.Num() >= MaxPreyCount)
        {
            break;
        }
        TryReproducePrey(P);
    }

    TArray<APredator*> PredatorSnapshot = Predators;
    for (APredator* D : PredatorSnapshot)
    {
        if (Predators.Num() >= MaxPredatorCount)
        {
            break;
        }
        TryReproducePredator(D);
    }
}

void AEntorno::TryReproducePrey(APresa* Parent)
{
    if (!Parent || !Parent->bAlive || Parent->Hambre <= 70 || Parent->ReproCooldown > 0)
    {
        return;
    }

    bool bHasMate = false;
    for (APresa* Other : Preys)
    {
        if (Other && Other != Parent && Other->bAlive && Other->Hambre > 50 && Manhattan(Parent->GridPos, Other->GridPos) <= 2)
        {
            bHasMate = true;
            break;
        }
    }
    if (!bHasMate)
    {
        return;
    }

    const int32 DesiredChildren = FMath::Min(FMath::RandRange(1, 3), MaxPreyCount - Preys.Num());
    TArray<FIntPoint> Cells = FindNearestEmptyCells(Parent->GridPos, DesiredChildren);
    UWorld* World = GetWorld();
    if (!World || !PreyClass)
    {
        return;
    }

    for (const FIntPoint& Pos : Cells)
    {
        APresa* Child = World->SpawnActor<APresa>(PreyClass, GridToWorld(Pos), FRotator::ZeroRotator);
        if (Child)
        {
            Child->GridPos = Pos;
            Child->Hambre = 50;
            Child->MaxHambre = Parent->MaxHambre;
            Child->bAlive = true;
            Child->ReproCooldown = 10;
            Child->StepsHambreCero = 0;
            Preys.Add(Child);
            TotalPreyReproductions++;
        }
    }

    if (Cells.Num() > 0)
    {
        Parent->Hambre = FMath::Max(0, Parent->Hambre - 20);
        Parent->ReproCooldown = 10;
    }
}

void AEntorno::TryReproducePredator(APredator* Parent)
{
    if (!Parent || !Parent->bAlive || Parent->Hambre <= 70 || Parent->ReproCooldown > 0)
    {
        return;
    }

    bool bHasMate = false;
    for (APredator* Other : Predators)
    {
        if (Other && Other != Parent && Other->bAlive && Other->Hambre > 50 && Manhattan(Parent->GridPos, Other->GridPos) <= 2)
        {
            bHasMate = true;
            break;
        }
    }
    if (!bHasMate)
    {
        return;
    }

    const int32 DesiredChildren = FMath::Min(FMath::RandRange(1, 3), MaxPredatorCount - Predators.Num());
    TArray<FIntPoint> Cells = FindNearestEmptyCells(Parent->GridPos, DesiredChildren);
    UWorld* World = GetWorld();
    if (!World || !PredatorClass)
    {
        return;
    }

    for (const FIntPoint& Pos : Cells)
    {
        APredator* Child = World->SpawnActor<APredator>(PredatorClass, GridToWorld(Pos), FRotator::ZeroRotator);
        if (Child)
        {
            Child->GridPos = Pos;
            Child->Hambre = 50;
            Child->MaxHambre = Parent->MaxHambre;
            Child->bAlive = true;
            Child->ReproCooldown = 10;
            Child->StepsHambreCero = 0;
            Predators.Add(Child);
            TotalPredatorReproductions++;
        }
    }

    if (Cells.Num() > 0)
    {
        Parent->Hambre = FMath::Max(0, Parent->Hambre - 20);
        Parent->ReproCooldown = 10;
    }
}

TArray<FIntPoint> AEntorno::FindNearestEmptyCells(const FIntPoint& Origin, int32 Count, int32 MaxDist) const
{
    TArray<FIntPoint> Free = GetFreeSpaces();
    Free.RemoveAll([this, Origin, MaxDist](const FIntPoint& Pos)
    {
        return Manhattan(Origin, Pos) > MaxDist;
    });

    Algo::Sort(Free, [this, Origin](const FIntPoint& A, const FIntPoint& B)
    {
        return Manhattan(Origin, A) < Manhattan(Origin, B);
    });

    if (Free.Num() > Count)
    {
        Free.SetNum(Count);
    }
    return Free;
}
