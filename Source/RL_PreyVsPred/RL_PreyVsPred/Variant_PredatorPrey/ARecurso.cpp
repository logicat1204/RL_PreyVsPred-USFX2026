#include "ARecurso.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"

ARecurso::ARecurso()
{
    PrimaryActorTick.bCanEverTick = false;

    MeshComp = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    RootComponent = MeshComp;

    static ConstructorHelpers::FObjectFinder<UStaticMesh> MeshAsset(TEXT("/Game/Fab/Small_garden_hay/small_garden_hay/StaticMeshes/small_garden_hay.small_garden_hay"));
    if (MeshAsset.Succeeded())
    {
        MeshComp->SetStaticMesh(MeshAsset.Object);
    }
    MeshComp->SetWorldScale3D(FVector(0.3f));
    MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}
