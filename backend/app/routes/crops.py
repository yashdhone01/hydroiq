from fastapi import APIRouter, Query, Request
from app.models.recommender import recommend_crops
from app.models.yield_estimator import estimate_yield

router = APIRouter(prefix="/crops", tags=["crops"])

@router.get("/recommend")
def get_recommendations(
    request:       Request,
    system_type:   str   = Query(...),
    area_sqft:     float = Query(...),
    target_market: str   = Query(...),
    budget:        float = Query(50000),
    top_n:         int   = Query(5)
):
    live_prices = getattr(request.app.state, 'live_prices', {})
    results = recommend_crops(
        system_type=system_type,
        area_sqft=area_sqft,
        target_market=target_market,
        budget=budget,
        top_n=top_n,
        live_prices=live_prices
    )
    return {
        "system_type":      system_type,
        "area_sqft":        area_sqft,
        "target_market":    target_market,
        "count":            len(results),
        "live_prices_used": len(live_prices) > 0,
        "recommendations":  results
    }

@router.get("/yield")
def get_yield_estimate(
    crop_id:          str   = Query(...),
    system_type:      str   = Query(...),
    area_sqft:        float = Query(...),
    experience_level: str   = Query("beginner")
):
    return estimate_yield(
        crop_id=crop_id,
        system_type=system_type,
        area_sqft=area_sqft,
        experience_level=experience_level
    )

@router.get("/list")
def list_crops():
    import json, os
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')
    with open(path, 'r') as f:
        data = json.load(f)
    return {"crops": data['crops']}