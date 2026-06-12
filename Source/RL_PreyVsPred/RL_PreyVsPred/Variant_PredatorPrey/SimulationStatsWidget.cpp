#include "SimulationStatsWidget.h"
#include "Components/VerticalBox.h"

void USimulationStatsWidget::NativeConstruct()
{
    Super::NativeConstruct();
    HideStats();
}

void USimulationStatsWidget::ShowPreyStats(int32 AlivePreys, int32 Resources, int32 TotalReproductions)
{
    if (TxtLabel) TxtLabel->SetText(FText::FromString("=== PRESAS ==="));
    if (TxtLine1) TxtLine1->SetText(FText::Format(FText::FromString("Presas: {0}"), FText::AsNumber(AlivePreys)));
    if (TxtLine2) TxtLine2->SetText(FText::Format(FText::FromString("Recursos: {0}"), FText::AsNumber(Resources)));
    if (TxtLine3) TxtLine3->SetText(FText::Format(FText::FromString("Reproducidas: {0}"), FText::AsNumber(TotalReproductions)));
    SetVisibility(ESlateVisibility::Visible);
}

void USimulationStatsWidget::ShowPredatorStats(int32 AlivePredators, int32 AvailablePreys, int32 TotalReproductions)
{
    if (TxtLabel) TxtLabel->SetText(FText::FromString("=== DEPREDADORES ==="));
    if (TxtLine1) TxtLine1->SetText(FText::Format(FText::FromString("Vivos: {0}"), FText::AsNumber(AlivePredators)));
    if (TxtLine2) TxtLine2->SetText(FText::Format(FText::FromString("Presas disponibles: {0}"), FText::AsNumber(AvailablePreys)));
    if (TxtLine3) TxtLine3->SetText(FText::Format(FText::FromString("Reproducidos: {0}"), FText::AsNumber(TotalReproductions)));
    SetVisibility(ESlateVisibility::Visible);
}

void USimulationStatsWidget::ShowPopulation(int32 PreyCount, int32 PredatorCount, float PreyPercent, float PredatorPercent)
{
    if (TxtLabel) TxtLabel->SetText(FText::FromString("=== POBLACION ==="));
    if (TxtLine1) TxtLine1->SetText(FText::Format(FText::FromString("Presas: {0}"), FText::AsNumber(PreyCount)));
    if (TxtLine2) TxtLine2->SetText(FText::Format(FText::FromString("Depredadores: {0}"), FText::AsNumber(PredatorCount)));
    if (TxtLine3)
    {
        FString PercentText = FString::Printf(TEXT("P: %.1f%%  D: %.1f%%"), PreyPercent, PredatorPercent);
        TxtLine3->SetText(FText::FromString(PercentText));
    }
    SetVisibility(ESlateVisibility::Visible);
}

void USimulationStatsWidget::HideStats()
{
    SetVisibility(ESlateVisibility::Hidden);
}

void USimulationStatsWidget::SetMode(EStatsMode NewMode)
{
    if (CurrentMode == NewMode)
    {
        HideStats();
        CurrentMode = EStatsMode::None;
        return;
    }
    CurrentMode = NewMode;
}
