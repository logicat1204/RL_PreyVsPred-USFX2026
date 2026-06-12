#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AEntorno.generated.h"

class APresa;
class APredator;
class ARecurso;

UENUM()
enum class EEntornoCellType : uint8
{
    Empty,
    Prey,
    Predator,
    Resource,
    Invalid
};

UCLASS()
class AEntorno : public AActor
{
    GENERATED_BODY()

public:
    AEntorno();

    UPROPERTY(EditAnywhere, Category = "Grid")
    int32 GridSizeX = 20;

    UPROPERTY(EditAnywhere, Category = "Grid")
    int32 GridSizeY = 20;

    UPROPERTY(EditAnywhere, Category = "Grid")
    float CellSize = 100.0f;

    UPROPERTY(EditAnywhere, Category = "Population")
    int32 InitialPreyCount = 5;

    UPROPERTY(EditAnywhere, Category = "Population")
    int32 InitialPredatorCount = 5;

    UPROPERTY(EditAnywhere, Category = "Population")
    int32 MaxResources = 15;

    UPROPERTY(EditAnywhere, Category = "Population")
    int32 MaxPreyCount = 80;

    UPROPERTY(EditAnywhere, Category = "Population")
    int32 MaxPredatorCount = 60;

    UPROPERTY(EditAnywhere, Category = "Classes")
    TSubclassOf<APresa> PreyClass;

    UPROPERTY(EditAnywhere, Category = "Classes")
    TSubclassOf<APredator> PredatorClass;

    UPROPERTY(VisibleAnywhere, Category = "Runtime")
    TArray<APresa*> Preys;

    UPROPERTY(VisibleAnywhere, Category = "Runtime")
    TArray<APredator*> Predators;

    TArray<FIntPoint> ResourcePositions;
    TArray<ARecurso*> ResourceMeshes;

    UPROPERTY(VisibleAnywhere, Category = "Stats")
    int32 TotalPreyReproductions = 0;

    UPROPERTY(VisibleAnywhere, Category = "Stats")
    int32 TotalPredatorReproductions = 0;

    void InitializeSimulation();
    void ResetSimulation();
    void Step();

    bool IsValidPos(const FIntPoint& Pos) const;
    bool IsFree(const FIntPoint& Pos) const;
    EEntornoCellType GetCellType(const FIntPoint& Pos) const;
    FVector GridToWorld(const FIntPoint& Pos) const;
    int32 Manhattan(const FIntPoint& A, const FIntPoint& B) const;

    TArray<FIntPoint> GetFreeSpaces() const;
    TArray<FIntPoint> GetPreyPositions() const;
    TArray<FIntPoint> GetPredatorPositions() const;
    TArray<FIntPoint> GetResourcePositions() const;

    void MovePrey(APresa* Prey, const FIntPoint& NewPos);
    void MovePredator(APredator* Pred, const FIntPoint& NewPos);
    APresa* GetPreyAt(const FIntPoint& Pos);
    APredator* GetPredatorAt(const FIntPoint& Pos);

    void SpawnResource();
    void RemoveResource(const FIntPoint& Pos);

    bool IsPreyAt(const FIntPoint& Pos) const;
    bool IsPredatorAt(const FIntPoint& Pos) const;
    bool IsResourceAt(const FIntPoint& Pos) const;

protected:
    virtual void BeginPlay() override;

private:
    FVector GridOrigin;

    void SpawnResources();
    void CleanupDeadAgents();
    void HandleReproduction();
    void TryReproducePrey(APresa* Parent);
    void TryReproducePredator(APredator* Parent);
    TArray<FIntPoint> FindNearestEmptyCells(const FIntPoint& Origin, int32 Count, int32 MaxDist = 15) const;
};
