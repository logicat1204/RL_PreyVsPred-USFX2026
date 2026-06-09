#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "AFacadeSimulation.generated.h"

class AEntorno;

UCLASS()
class AFacadeSimulation : public AActor
{
    GENERATED_BODY()

public:
    AFacadeSimulation();

    UFUNCTION(BlueprintCallable, Category = "Simulation")
    void StartSimulation();

    UFUNCTION(BlueprintCallable, Category = "Simulation")
    void StopSimulation();

    UFUNCTION(BlueprintCallable, Category = "Simulation")
    void StepSimulation();

    UFUNCTION(BlueprintCallable, Category = "Simulation")
    void ResetSimulation();

    UPROPERTY(EditAnywhere, Category = "Simulation")
    AEntorno* Entorno;

    UPROPERTY(EditAnywhere, Category = "Simulation")
    int32 StepsPerSecond = 2;

    UPROPERTY(EditAnywhere, Category = "Simulation")
    int32 MaxSteps = 0;

    UPROPERTY(EditAnywhere, Category = "Simulation")
    bool bAutoStartOnBeginPlay = false;

    UPROPERTY(VisibleAnywhere, Category = "Simulation")
    int32 CurrentStep = 0;

    UPROPERTY(VisibleAnywhere, Category = "Simulation")
    bool bSimulationRunning = false;

    UPROPERTY(VisibleAnywhere, Category = "Simulation")
    bool bSimulationFinished = false;

protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

private:
    FTimerHandle SimulationTimerHandle;

    void OnSimulationTick();

    void LogStats();
};
