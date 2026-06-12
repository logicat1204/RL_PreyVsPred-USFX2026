// Copyright Epic Games, Inc. All Rights Reserved.

#include "RL_PreyVsPredGameMode.h"
#include "RL_PreyVsPred/Variant_PredatorPrey/AFacadeSimulation.h"
#include "RL_PreyVsPred/Variant_PredatorPrey/AEntorno.h"
#include "RL_PreyVsPred/Variant_PredatorPrey/APresa.h"
#include "RL_PreyVsPred/Variant_PredatorPrey/APredator.h"
#include "RL_PreyVsPred/Variant_PredatorPrey/SimulationStatsWidget.h"
#include "Engine/World.h"
#include "Components/InputComponent.h"
#include "GameFramework/PlayerController.h"

ARL_PreyVsPredGameMode::ARL_PreyVsPredGameMode()
{
	PrimaryActorTick.bCanEverTick = true;
}

void ARL_PreyVsPredGameMode::BeginPlay()
{
	Super::BeginPlay();

	if (FacadeClass)
	{
		FActorSpawnParameters SpawnParams;
		SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		SimulationFacade = GetWorld()->SpawnActor<AFacadeSimulation>(FacadeClass, FVector::ZeroVector, FRotator::ZeroRotator, SpawnParams);
		StartSimulation();
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[GameMode] FacadeClass not set — assign a BP of AFacadeSimulation"));
	}

	FTimerHandle TimerHandle;
	GetWorldTimerManager().SetTimer(TimerHandle, this, &ARL_PreyVsPredGameMode::SetupInputAndWidget, 0.1f, false);
}

void ARL_PreyVsPredGameMode::SetupInputAndWidget()
{
	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	if (!PC) return;

	if (StatsWidgetClass)
	{
		StatsWidget = CreateWidget<USimulationStatsWidget>(PC, StatsWidgetClass);
		if (StatsWidget)
		{
			StatsWidget->AddToViewport(100);
		}
	}

	EnableInput(PC);
	if (InputComponent)
	{
		InputComponent->BindKey(EKeys::P, IE_Pressed, this, &ARL_PreyVsPredGameMode::TogglePreyStats);
		InputComponent->BindKey(EKeys::F, IE_Pressed, this, &ARL_PreyVsPredGameMode::TogglePredatorStats);
		InputComponent->BindKey(EKeys::Tab, IE_Pressed, this, &ARL_PreyVsPredGameMode::TogglePopulation);
	}
}

void ARL_PreyVsPredGameMode::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	UpdateStatsWidget();
}

void ARL_PreyVsPredGameMode::TogglePreyStats()
{
	if (!StatsWidget || !GetEntorno()) return;

	EStatsMode Mode = StatsWidget->GetMode();
	if (Mode == EStatsMode::Prey)
	{
		StatsWidget->SetMode(EStatsMode::None);
		StatsWidget->HideStats();
		return;
	}

	StatsWidget->SetMode(EStatsMode::Prey);
	UpdateStatsWidget();
}

void ARL_PreyVsPredGameMode::TogglePredatorStats()
{
	if (!StatsWidget || !GetEntorno()) return;

	EStatsMode Mode = StatsWidget->GetMode();
	if (Mode == EStatsMode::Predator)
	{
		StatsWidget->SetMode(EStatsMode::None);
		StatsWidget->HideStats();
		return;
	}

	StatsWidget->SetMode(EStatsMode::Predator);
	UpdateStatsWidget();
}

void ARL_PreyVsPredGameMode::TogglePopulation()
{
	if (!StatsWidget || !GetEntorno()) return;

	EStatsMode Mode = StatsWidget->GetMode();
	if (Mode == EStatsMode::Population)
	{
		StatsWidget->SetMode(EStatsMode::None);
		StatsWidget->HideStats();
		return;
	}

	StatsWidget->SetMode(EStatsMode::Population);
	UpdateStatsWidget();
}

void ARL_PreyVsPredGameMode::UpdateStatsWidget()
{
	if (!StatsWidget || !GetEntorno()) return;

	EStatsMode Mode = StatsWidget->GetMode();
	if (Mode == EStatsMode::None) return;

	AEntorno* Env = GetEntorno();

	int32 AlivePreys = 0;
	for (auto* P : Env->Preys) { if (P && P->bAlive) AlivePreys++; }

	int32 AlivePreds = 0;
	for (auto* D : Env->Predators) { if (D && D->bAlive) AlivePreds++; }

	switch (Mode)
	{
	case EStatsMode::Prey:
		StatsWidget->ShowPreyStats(AlivePreys, Env->GetResourcePositions().Num(), Env->TotalPreyReproductions);
		break;

	case EStatsMode::Predator:
		StatsWidget->ShowPredatorStats(AlivePreds, AlivePreys, Env->TotalPredatorReproductions);
		break;

	case EStatsMode::Population:
	{
		int32 Total = AlivePreys + AlivePreds;
		float PctP = Total > 0 ? (100.0f * AlivePreys / Total) : 0.0f;
		float PctD = Total > 0 ? (100.0f * AlivePreds / Total) : 0.0f;
		StatsWidget->ShowPopulation(AlivePreys, AlivePreds, PctP, PctD);
		break;
	}
	default:
		break;
	}
}

AEntorno* ARL_PreyVsPredGameMode::GetEntorno() const
{
	return SimulationFacade ? SimulationFacade->Entorno : nullptr;
}

void ARL_PreyVsPredGameMode::StartSimulation()
{
	if (SimulationFacade)
	{
		SimulationFacade->StartSimulation();
	}
}

void ARL_PreyVsPredGameMode::StopSimulation()
{
	if (SimulationFacade)
	{
		SimulationFacade->StopSimulation();
	}
}
