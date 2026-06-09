#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ARecurso.generated.h"

UCLASS()
class ARecurso : public AActor
{
    GENERATED_BODY()

public:
    ARecurso();

    UPROPERTY(VisibleAnywhere, Category = "Mesh")
    UStaticMeshComponent* MeshComp;

    UPROPERTY()
    FIntPoint GridPos;
};
