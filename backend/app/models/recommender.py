import json
import os
import pandas as pd
from typing import List

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')

def load_crops() -> pd.DataFrame:
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['crops'])

def recommend_crops(
    system_type:   str,
    area_sqft:     float,
    target_market: str,
    budget:        float,
    top_n:         int  = 5,
    live_prices:   dict = None
) -> List[dict]:
    if live_prices is None:
        live_prices = {}

    df = load_crops()
    df = df[df['systems'].apply(lambda s: system_type in s)].copy()

    if df.empty:
        return []

    # convert to float and apply live mandi prices
    df['local_price_per_kg'] = df['local_price_per_kg'].astype(float)

    # price priority: live > historical > static
    # apply historical avg prices first (for crops without live prices)
    try:
        from app.services.data_pipeline import get_historical_avg_prices
        historical = get_historical_avg_prices()
        for crop_id, price in historical.items():
            if crop_id not in live_prices:
                df.loc[df['id'] == crop_id, 'local_price_per_kg'] = float(price)
    except Exception:
        historical = {}

    # apply live prices (highest priority)
    for crop_id, price in live_prices.items():
        df.loc[df['id'] == crop_id, 'local_price_per_kg'] = float(price)

    if target_market == 'export':
        df['price_per_kg'] = df['export_price_per_kg'].astype(float)
    else:
        df['price_per_kg'] = df['local_price_per_kg']

    df['yield_per_cycle_kg']     = df['yield_per_sqft_kg'] * area_sqft
    df['revenue_per_cycle']      = df['yield_per_cycle_kg'] * df['price_per_kg']
    df['annual_revenue']         = df['revenue_per_cycle'] * df['cycles_per_year']
    df['water_per_cycle_liters'] = df['water_liters_per_sqft'] * area_sqft
    df['roi_score']              = df['annual_revenue'] / area_sqft
    df = df.sort_values('roi_score', ascending=False).head(top_n)

    result = []
    for _, row in df.iterrows():
        result.append({
            'id':                     row['id'],
            'name':                   row['name'],
            'difficulty':             row['difficulty'],
            'growth_days':            int(row['growth_days']),
            'cycles_per_year':        int(row['cycles_per_year']),
            'yield_per_cycle_kg':     round(float(row['yield_per_cycle_kg']), 2),
            'revenue_per_cycle':      round(float(row['revenue_per_cycle']), 2),
            'annual_revenue':         round(float(row['annual_revenue']), 2),
            'price_per_kg':           round(float(row['price_per_kg']), 2),
            'local_price_per_kg':     round(float(row['local_price_per_kg']), 2),
            'water_per_cycle_liters': round(float(row['water_per_cycle_liters']), 2),
            'export_markets':         row['export_markets'],
            'roi_score':              round(float(row['roi_score']), 2),
            'price_source':           'live' if row['id'] in live_prices else ('historical' if row['id'] in historical else 'static')
        })

    return result