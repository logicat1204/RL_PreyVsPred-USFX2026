#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/TextBlock.h"
#include "SimulationStatsWidget.generated.h"

UENUM()
enum class EStatsMode : uint8
{
    None,
    Prey,
    Predator,
    Population
};

UCLASS()
class USimulationStatsWidget : public UUserWidget
{
    GENERATED_BODY()

public:
    virtual void NativeConstruct() override;

    void ShowPreyStats(int32 AlivePreys, int32 Resources, int32 TotalReproductions);
    void ShowPredatorStats(int32 AlivePredators, int32 AvailablePreys, int32 TotalReproductions);
    void ShowPopulation(int32 PreyCount, int32 PredatorCount, float PreyPercent, float PredatorPercent);
    void HideStats();

    void SetMode(EStatsMode NewMode);
    EStatsMode GetMode() const { return CurrentMode; }

protected:
    UPROPERTY(meta = (BindWidget))
    UTextBlock* TxtLabel;

    UPROPERTY(meta = (BindWidget))
    UTextBlock* TxtLine1;

    UPROPERTY(meta = (BindWidget))
    UTextBlock* TxtLine2;

    UPROPERTY(meta = (BindWidget))
    UTextBlock* TxtLine3;

private:
    EStatsMode CurrentMode = EStatsMode::None;
};
