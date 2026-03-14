import json
import os
import pandas as pd
from typing import List, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')

def load_crops() -> pd.DataFrame:
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['crops'])

def recommend_crops(
    system_type: str,
    area_sqft: float,
    target_market: str,  # 'local' or 'export'
    budget: float,
    top_n: int = 5
) -> List[dict]:
    df = load_crops()

    # filter by system compatibility
    df = df[df['systems'].apply(lambda s: system_type in s)]

    if df.empty:
        return []

    # calculate revenue based on target market
    if target_market == 'export':
        df['price_per_kg'] = df['export_price_per_kg']
    else:
        df['price_per_kg'] = df['local_price_per_kg']

    # calculate metrics per cycle
    df['yield_per_cycle_kg']    = df['yield_per_sqft_kg'] * area_sqft
    df['revenue_per_cycle']     = df['yield_per_cycle_kg'] * df['price_per_kg']
    df['annual_revenue']        = df['revenue_per_cycle'] * df['cycles_per_year']
    df['water_per_cycle_liters']= df['water_liters_per_sqft'] * area_sqft

    # simple ROI score — annual revenue per sqft
    df['roi_score'] = df['annual_revenue'] / area_sqft

    # sort by ROI
    df = df.sort_values('roi_score', ascending=False).head(top_n)

    result = []
    for _, row in df.iterrows():
        result.append({
            'id':                    row['id'],
            'name':                  row['name'],
            'difficulty':            row['difficulty'],
            'growth_days':           int(row['growth_days']),
            'cycles_per_year':       int(row['cycles_per_year']),
            'yield_per_cycle_kg':    round(row['yield_per_cycle_kg'], 2),
            'revenue_per_cycle':     round(row['revenue_per_cycle'], 2),
            'annual_revenue':        round(row['annual_revenue'], 2),
            'price_per_kg':          round(row['price_per_kg'], 2),
            'water_per_cycle_liters':round(row['water_per_cycle_liters'], 2),
            'export_markets':        row['export_markets'],
            'roi_score':             round(row['roi_score'], 2)
        })

    return result