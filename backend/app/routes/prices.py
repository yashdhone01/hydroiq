from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from app.models.price_predictor import predict_price
from app.services.data_pipeline import get_historical_avg_prices, get_price_stats

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/predict")
def price_prediction(
    crop_id:      str = Query(..., description="Crop ID e.g. basil, mint, lettuce"),
    region:       str = Query("National", description="Region: North, South, East, West, or National"),
    months_ahead: int = Query(1, description="Months ahead to predict (1-12)", ge=1, le=12)
):
    try:
        return predict_price(
            crop_id=crop_id,
            region=region,
            months_ahead=months_ahead
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/historical")
def historical_prices(
    crop_id: str = Query(None, description="Specific crop ID, or leave empty for all")
):
    if crop_id:
        stats = get_price_stats(crop_id)
        if 'error' in stats:
            raise HTTPException(status_code=404, detail=stats['error'])
        return stats
    else:
        return {
            "source": "historical dataset",
            "prices": get_historical_avg_prices()
        }
