from fastapi import APIRouter, Query
from app.models.yield_estimator import calculate_roi

router = APIRouter(prefix="/roi", tags=["roi"])

@router.get("/calculate")
def get_roi(
    crop_id:                str   = Query(..., description="Crop ID e.g. basil"),
    system_type:            str   = Query(..., description="NFT, DWC, or Kratky"),
    area_sqft:              float = Query(..., description="Area in sq ft"),
    target_market:          str   = Query(..., description="local or export"),
    setup_cost:             float = Query(..., description="One-time setup cost in INR"),
    monthly_operating_cost: float = Query(..., description="Monthly operating cost in INR"),
    experience_level:       str   = Query("beginner", description="beginner, intermediate, expert")
):
    result = calculate_roi(
        crop_id=crop_id,
        system_type=system_type,
        area_sqft=area_sqft,
        target_market=target_market,
        setup_cost=setup_cost,
        monthly_operating_cost=monthly_operating_cost,
        experience_level=experience_level
    )
    return result

@router.get("/compare")
def compare_crops_roi(
    system_type:            str   = Query(..., description="NFT, DWC, or Kratky"),
    area_sqft:              float = Query(..., description="Area in sq ft"),
    target_market:          str   = Query(..., description="local or export"),
    setup_cost:             float = Query(..., description="Setup cost in INR"),
    monthly_operating_cost: float = Query(..., description="Monthly operating cost in INR"),
    experience_level:       str   = Query("beginner")
):
    from app.models.recommender import load_crops
    df = load_crops()
    df = df[df['systems'].apply(lambda s: system_type in s)]

    results = []
    for _, row in df.iterrows():
        roi = calculate_roi(
            crop_id=row['id'],
            system_type=system_type,
            area_sqft=area_sqft,
            target_market=target_market,
            setup_cost=setup_cost,
            monthly_operating_cost=monthly_operating_cost,
            experience_level=experience_level
        )
        if 'error' not in roi:
            results.append(roi)

    results = sorted(results, key=lambda x: x['annual_profit'], reverse=True)

    return {
        "system_type":   system_type,
        "area_sqft":     area_sqft,
        "target_market": target_market,
        "count":         len(results),
        "comparison":    results
    }