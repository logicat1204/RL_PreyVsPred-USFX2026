// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "RL_PreyVsPredGameMode.generated.h"

class AFacadeSimulation;
class USimulationStatsWidget;
class AEntorno;

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
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Simulation")
	TSubclassOf<AFacadeSimulation> FacadeClass;

	UPROPERTY(VisibleInstanceOnly, Category = "Simulation")
	AFacadeSimulation* SimulationFacade;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "UI")
	TSubclassOf<USimulationStatsWidget> StatsWidgetClass;

	UPROPERTY(VisibleInstanceOnly, Category = "UI")
	USimulationStatsWidget* StatsWidget;

	void TogglePreyStats();
	void TogglePredatorStats();
	void TogglePopulation();
	void UpdateStatsWidget();
	void SetupInputAndWidget();

	AEntorno* GetEntorno() const;
};
