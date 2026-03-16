from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from app.models.yield_estimator import calculate_roi

router = APIRouter(prefix="/roi", tags=["roi"])

SystemType      = Literal['NFT', 'DWC', 'Kratky']
TargetMarket    = Literal['local', 'export']
ExperienceLevel = Literal['beginner', 'intermediate', 'expert']

@router.get("/calculate")
def get_roi(
    crop_id:                str             = Query(..., description="Crop ID e.g. basil"),
    system_type:            SystemType      = Query(..., description="NFT, DWC, or Kratky"),
    area_sqft:              float           = Query(..., description="Area in sq ft", gt=0),
    target_market:          TargetMarket    = Query(..., description="local or export"),
    setup_cost:             float           = Query(..., description="One-time setup cost in INR", gt=0),
    monthly_operating_cost: float           = Query(..., description="Monthly operating cost in INR", ge=0),
    experience_level:       ExperienceLevel = Query("beginner", description="beginner, intermediate, expert"),
    water_cost_per_liter:   float           = Query(0.0, description="Water cost per liter in INR", ge=0)
):
    try:
        return calculate_roi(
            crop_id=crop_id,
            system_type=system_type,
            area_sqft=area_sqft,
            target_market=target_market,
            setup_cost=setup_cost,
            monthly_operating_cost=monthly_operating_cost,
            experience_level=experience_level,
            water_cost_per_liter=water_cost_per_liter
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/compare")
def compare_crops_roi(
    system_type:            SystemType      = Query(..., description="NFT, DWC, or Kratky"),
    area_sqft:              float           = Query(..., description="Area in sq ft", gt=0),
    target_market:          TargetMarket    = Query(..., description="local or export"),
    setup_cost:             float           = Query(..., description="Setup cost in INR", gt=0),
    monthly_operating_cost: float           = Query(..., description="Monthly operating cost in INR", ge=0),
    experience_level:       ExperienceLevel = Query("beginner"),
    water_cost_per_liter:   float           = Query(0.0, description="Water cost per liter in INR", ge=0)
):
    from app.models.recommender import load_crops
    df = load_crops()
    df = df[df['systems'].apply(lambda s: system_type in s)]

    results = []
    for _, row in df.iterrows():
        try:
            roi = calculate_roi(
                crop_id=row['id'],
                system_type=system_type,
                area_sqft=area_sqft,
                target_market=target_market,
                setup_cost=setup_cost,
                monthly_operating_cost=monthly_operating_cost,
                experience_level=experience_level,
                water_cost_per_liter=water_cost_per_liter
            )
            results.append(roi)
        except ValueError:
            continue

    results = sorted(results, key=lambda x: x['annual_profit'], reverse=True)

    return {
        "system_type":   system_type,
        "area_sqft":     area_sqft,
        "target_market": target_market,
        "count":         len(results),
        "comparison":    results
    }