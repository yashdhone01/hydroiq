"""
Price prediction inference — predict future crop prices.

Uses the trained GradientBoosting model to forecast prices
given crop, region, and target month.
"""

import os
import joblib
import numpy as np
import pandas as pd
from app.services.data_pipeline import load_and_clean

SAVE_DIR = os.path.join(os.path.dirname(__file__), 'saved')


def _load_model():
    """Load the trained price model and encoders."""
    model     = joblib.load(os.path.join(SAVE_DIR, 'price_model.pkl'))
    le_crop   = joblib.load(os.path.join(SAVE_DIR, 'price_le_crop.pkl'))
    le_region = joblib.load(os.path.join(SAVE_DIR, 'price_le_region.pkl'))
    metrics   = joblib.load(os.path.join(SAVE_DIR, 'price_metrics.pkl'))
    return model, le_crop, le_region, metrics


def predict_price(
    crop_id: str,
    region: str = 'National',
    months_ahead: int = 1
) -> dict:
    """
    Predict future price for a crop in a given region.

    Returns predicted price, confidence interval, and seasonal trend.
    """
    model_path = os.path.join(SAVE_DIR, 'price_model.pkl')
    if not os.path.exists(model_path):
        raise RuntimeError("Price model not trained yet. Restart the server to train.")

    model, le_crop, le_region, metrics = _load_model()
    df = load_and_clean()

    # validate crop_id
    if crop_id not in le_crop.classes_:
        raise ValueError(f"Unknown crop: {crop_id}")

    # handle unknown region gracefully
    if region not in le_region.classes_:
        region = le_region.classes_[0]  # fallback to first known region

    # get latest data for this crop to compute features
    crop_df = df[df['crop_id'] == crop_id].sort_values('date')
    if crop_df.empty:
        raise ValueError(f"No historical data for {crop_id}")

    # compute current features from latest data
    recent = crop_df.tail(30)
    current_price    = recent['modal_price'].mean()
    rolling_avg_30   = recent['modal_price'].mean()
    rolling_avg_90   = crop_df.tail(90)['modal_price'].mean()
    volatility       = recent['modal_price'].std() if len(recent) > 1 else 0
    price_trend      = (recent['modal_price'].iloc[-1] / recent['modal_price'].iloc[0] - 1) if len(recent) > 1 else 0
    price_spread     = ((recent['max_price'].mean() - recent['min_price'].mean()) /
                        recent['modal_price'].mean()) if recent['modal_price'].mean() > 0 else 0

    # determine target month/quarter
    from datetime import datetime, timedelta
    target_date = datetime.now() + timedelta(days=30 * months_ahead)
    target_month   = target_date.month
    target_quarter = (target_month - 1) // 3 + 1

    # build feature vector
    features = pd.DataFrame([{
        'crop_enc':       le_crop.transform([crop_id])[0],
        'region_enc':     le_region.transform([region])[0],
        'month':          target_month,
        'quarter':        target_quarter,
        'rolling_avg_30': rolling_avg_30,
        'rolling_avg_90': rolling_avg_90,
        'volatility':     volatility,
        'price_trend':    price_trend,
        'price_spread':   price_spread,
    }])

    predicted_price = float(model.predict(features)[0])

    # confidence interval based on model MAE
    mae = metrics.get('mae', 10)
    confidence_low  = round(max(0, predicted_price - 1.5 * mae), 2)
    confidence_high = round(predicted_price + 1.5 * mae, 2)

    # seasonal analysis — compare predicted month to yearly average
    monthly_avg = crop_df.groupby('month')['modal_price'].mean()
    yearly_avg  = crop_df['modal_price'].mean()
    month_avg   = monthly_avg.get(target_month, yearly_avg)

    if month_avg > yearly_avg * 1.08:
        seasonal_trend = 'high_season'
    elif month_avg < yearly_avg * 0.92:
        seasonal_trend = 'low_season'
    else:
        seasonal_trend = 'stable'

    # price direction
    if predicted_price > current_price * 1.05:
        direction = 'rising'
    elif predicted_price < current_price * 0.95:
        direction = 'falling'
    else:
        direction = 'stable'

    return {
        'crop_id':          crop_id,
        'region':           region,
        'months_ahead':     months_ahead,
        'current_price':    round(current_price, 2),
        'predicted_price':  round(predicted_price, 2),
        'confidence_low':   confidence_low,
        'confidence_high':  confidence_high,
        'direction':        direction,
        'seasonal_trend':   seasonal_trend,
        'model_accuracy': {
            'mae': round(metrics.get('mae', 0), 2),
            'r2':  round(metrics.get('r2', 0), 4),
        }
    }
