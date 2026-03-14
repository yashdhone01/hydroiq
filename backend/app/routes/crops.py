from fastapi import APIRouter, Query
from app.models.recommender import recommend_crops
from app.models.yield_estimator import estimate_yield

router = APIRouter(prefix="/crops", tags=["crops"])

@router.get("/recommend")
def get_recommendations(
    system_type:   str   = Query(..., description="NFT, DWC, or Kratky"),
    area_sqft:     float = Query(..., description="Available area in sq ft"),
    target_market: str   = Query(..., description="local or export"),
    budget:        float = Query(50000, description="Setup budget in INR"),
    top_n:         int   = Query(5, description="Number of recommendations")
):
    results = recommend_crops(
        system_type=system_type,
        area_sqft=area_sqft,
        target_market=target_market,
        budget=budget,
        top_n=top_n
    )
    return {
        "system_type":   system_type,
        "area_sqft":     area_sqft,
        "target_market": target_market,
        "count":         len(results),
        "recommendations": results
    }

@router.get("/yield")
def get_yield_estimate(
    crop_id:          str   = Query(..., description="Crop ID e.g. basil"),
    system_type:      str   = Query(..., description="NFT, DWC, or Kratky"),
    area_sqft:        float = Query(..., description="Area in sq ft"),
    experience_level: str   = Query("beginner", description="beginner, intermediate, expert")
):
    result = estimate_yield(
        crop_id=crop_id,
        system_type=system_type,
        area_sqft=area_sqft,
        experience_level=experience_level
    )
    return result

@router.get("/list")
def list_crops():
    import json, os
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')
    with open(path, 'r') as f:
        data = json.load(f)
    return {"crops": data['crops']}