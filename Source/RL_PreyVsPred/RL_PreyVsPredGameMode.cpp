// Copyright Epic Games, Inc. All Rights Reserved.

#include "RL_PreyVsPredGameMode.h"
#include "RL_PreyVsPred/Variant_PredatorPrey/AFacadeSimulation.h"
#include "Engine/World.h"

ARL_PreyVsPredGameMode::ARL_PreyVsPredGameMode()
{
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
