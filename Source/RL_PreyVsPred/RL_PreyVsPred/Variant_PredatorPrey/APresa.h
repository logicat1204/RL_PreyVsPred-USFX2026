#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "APresa.generated.h"

class AEntorno;

UCLASS()
class APresa : public AActor
{
    GENERATED_BODY()

public:
    APresa();

    UPROPERTY(VisibleAnywhere, Category = "Mesh")
    UStaticMeshComponent* MeshComp;

    UPROPERTY(VisibleAnywhere, Category = "State")
    FIntPoint GridPos;

    UPROPERTY(EditAnywhere, Category = "State")
    int32 Hambre = 100;

    UPROPERTY(EditAnywhere, Category = "State")
    int32 MaxHambre = 100;

    UPROPERTY(VisibleAnywhere, Category = "State")
    bool bAlive = true;

    UPROPERTY(VisibleAnywhere, Category = "State")
    int32 ReproCooldown = 0;

    UPROPERTY(VisibleAnywhere, Category = "State")
    int32 StepsHambreCero = 0;

    UPROPERTY(EditAnywhere, Category = "QTable")
    FString QTableFilePath = TEXT("Training/Prey_QTable.json");

    void LoadQTable();
    int32 GetState(AEntorno* Entorno);
    void ApplyAction(int32 ActionIdx, AEntorno* Entorno);
    int32 ChooseAction(int32 StateIdx);

    virtual void Tick(float DeltaTime) override;

    UPROPERTY(EditAnywhere, Category = "Movement")
    float PositionInterpSpeed = 6.0f;

    UPROPERTY(EditAnywhere, Category = "Movement")
    float RotationInterpSpeed = 8.0f;

    FVector TargetWorldLocation;
    FRotator TargetRotation;
    bool bMoving = false;

    TArray<TArray<float>> QTable;
    int32 NumStates = 1350;
    int32 NumActions = 5;

    static const int32 RS_LEVELS = 3;
    static const int32 RD_LEVELS = 5;
    static const int32 HB_LEVELS = 3;
    static const int32 RR_LEVELS = 2;
    static const int32 PR_LEVELS = 3;
    static const int32 PD_LEVELS = 5;

    static TArray<FIntPoint> DirOffsets;

protected:
    virtual void BeginPlay() override;

private:
    bool bQTableLoaded = false;
};
