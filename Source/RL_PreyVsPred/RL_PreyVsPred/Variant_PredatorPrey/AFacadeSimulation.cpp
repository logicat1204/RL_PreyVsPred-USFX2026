#include "AFacadeSimulation.h"
#include "AEntorno.h"
#include "APresa.h"
#include "APredator.h"
#include "Engine/World.h"

AFacadeSimulation::AFacadeSimulation()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AFacadeSimulation::BeginPlay()
{
    Super::BeginPlay();

    if (bAutoStartOnBeginPlay)
    {
        StartSimulation();
    }
}

void AFacadeSimulation::StartSimulation()
{
    if (bSimulationRunning)
    {
        UE_LOG(LogTemp, Warning, TEXT("[Facade] Already running"));
        return;
    }

    if (!Entorno)
    {
        UE_LOG(LogTemp, Error, TEXT("[Facade] Entorno not assigned! Open BP_FacadeSimulation and assign Entorno."));
        return;
    }

    Entorno->InitializeSimulation();

    if (Entorno->Preys.Num() == 0 && Entorno->Predators.Num() == 0)
    {
        UE_LOG(LogTemp, Error, TEXT("[Facade] No agents spawned — check PreyClass/PredatorClass in BP_Entorno"));
    }

    CurrentStep = 0;
    bSimulationFinished = false;
    bSimulationRunning = true;

    float Interval = 1.0f / FMath::Max(1, StepsPerSecond);
    GetWorldTimerManager().SetTimer(SimulationTimerHandle, this,
        &AFacadeSimulation::OnSimulationTick, Interval, true);

    LogStats();
    UE_LOG(LogTemp, Log, TEXT("[Facade] Simulation started (%d steps/sec, interval=%.2fs)"),
           StepsPerSecond, Interval);
}

void AFacadeSimulation::StopSimulation()
{
    if (!bSimulationRunning) return;

    bSimulationRunning = false;
    GetWorldTimerManager().ClearTimer(SimulationTimerHandle);

    UE_LOG(LogTemp, Log, TEXT("[Facade] Simulation stopped at step %d"), CurrentStep);
}

void AFacadeSimulation::StepSimulation()
{
    if (!Entorno)
    {
        UE_LOG(LogTemp, Error, TEXT("[Facade] StepSimulation: Entorno is null"));
        return;
    }

    Entorno->Step();
    CurrentStep++;

    if (CurrentStep % 5 == 0 || CurrentStep == 1)
    {
        LogStats();
    }

    if (MaxSteps > 0 && CurrentStep >= MaxSteps)
    {
        StopSimulation();
        bSimulationFinished = true;
        UE_LOG(LogTemp, Log, TEXT("[Facade] Simulation finished (%d steps)"), CurrentStep);
    }
}

void AFacadeSimulation::ResetSimulation()
{
    StopSimulation();
    if (Entorno)
    {
        Entorno->ResetSimulation();
    }
    CurrentStep = 0;
    bSimulationFinished = false;
    UE_LOG(LogTemp, Log, TEXT("[Facade] Simulation reset"));
}

void AFacadeSimulation::OnSimulationTick()
{
    if (bSimulationRunning)
    {
        StepSimulation();
    }
}

void AFacadeSimulation::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}

void AFacadeSimulation::LogStats()
{
    if (!Entorno) return;

    int32 AlivePreys = 0;
    for (auto* P : Entorno->Preys)
    {
        if (P && P->bAlive) AlivePreys++;
    }

    int32 AlivePreds = 0;
    for (auto* D : Entorno->Predators)
    {
        if (D && D->bAlive) AlivePreds++;
    }

    int32 Total = AlivePreys + AlivePreds;
    float PctP = Total > 0 ? (100.0f * AlivePreys / Total) : 0.0f;
    float PctD = Total > 0 ? (100.0f * AlivePreds / Total) : 0.0f;

    int32 NumResources = Entorno->GetResourcePositions().Num();

    UE_LOG(LogTemp, Log, TEXT("[Facade] Step %d | Preys: %d (%.0f%%) Preds: %d (%.0f%%) Resources: %d"),
           CurrentStep, AlivePreys, PctP, AlivePreds, PctD, NumResources);
}
