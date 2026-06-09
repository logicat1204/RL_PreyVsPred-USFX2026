// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "RL_PreyVsPredGameMode.generated.h"

class AFacadeSimulation;

UCLASS()
class ARL_PreyVsPredGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	ARL_PreyVsPredGameMode();

	UFUNCTION(BlueprintCallable, Category = "Simulation")
	void StartSimulation();

	UFUNCTION(BlueprintCallable, Category = "Simulation")
	void StopSimulation();

protected:
	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Simulation")
	TSubclassOf<AFacadeSimulation> FacadeClass;

	UPROPERTY(VisibleInstanceOnly, Category = "Simulation")
	AFacadeSimulation* SimulationFacade;
};



