#pragma once

#include "CoreMinimal.h"

class AEntorno;

inline int32 DirectionTo(const FIntPoint& Src, const FIntPoint& Dst)
{
    const int32 Dx = Dst.X - Src.X;
    const int32 Dy = Dst.Y - Src.Y;
    if (Dx == 0 && Dy == 0) return 0;
    if (FMath::Abs(Dx) >= FMath::Abs(Dy))
        return Dx < 0 ? 1 : 2;
    return Dy < 0 ? 3 : 4;
}

inline void NearestInfo(AEntorno* Entorno, const FIntPoint& Src, const TArray<FIntPoint>& Positions, int32& OutDist, int32& OutDir)
{
    OutDist = -1;
    OutDir = 0;
    for (const FIntPoint& Pos : Positions)
    {
        const int32 Dist = Entorno->Manhattan(Src, Pos);
        if (OutDist < 0 || Dist < OutDist)
        {
            OutDist = Dist;
            OutDir = DirectionTo(Src, Pos);
        }
    }
}
