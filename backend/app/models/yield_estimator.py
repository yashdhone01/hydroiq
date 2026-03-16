import json
import os
import pandas as pd
from typing import Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')

def load_crops() -> pd.DataFrame:
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['crops'])

# multipliers based on system efficiency
SYSTEM_MULTIPLIERS = {
    'NFT':   1.0,
    'DWC':   1.15,  # 15% better than baseline
    'Kratky': 0.85  # 15% less than baseline
}

def estimate_yield(
    crop_id: str,
    system_type: str,
    area_sqft: float,
    experience_level: str = 'beginner'  # beginner, intermediate, expert
) -> dict:
    df = load_crops()
    crop = df[df['id'] == crop_id]

    if crop.empty:
        raise ValueError(f'Crop {crop_id} not found')

    crop = crop.iloc[0]

    # experience multiplier
    experience_multipliers = {
        'beginner':     0.7,
        'intermediate': 0.9,
        'expert':       1.0
    }

    system_mult     = SYSTEM_MULTIPLIERS.get(system_type, 1.0)
    experience_mult = experience_multipliers.get(experience_level, 0.9)

    base_yield          = crop['yield_per_sqft_kg'] * area_sqft
    adjusted_yield      = base_yield * system_mult * experience_mult
    annual_yield        = adjusted_yield * crop['cycles_per_year']

    return {
        'crop_name':            crop['name'],
        'system_type':          system_type,
        'area_sqft':            area_sqft,
        'experience_level':     experience_level,
        'yield_per_cycle_kg':   round(adjusted_yield, 2),
        'cycles_per_year':      int(crop['cycles_per_year']),
        'annual_yield_kg':      round(annual_yield, 2),
        'growth_days':          int(crop['growth_days']),
        'system_efficiency':    f"{int(system_mult * 100)}%",
        'experience_efficiency':f"{int(experience_mult * 100)}%"
    }

def calculate_roi(
    crop_id: str,
    system_type: str,
    area_sqft: float,
    target_market: str,
    setup_cost: float,
    monthly_operating_cost: float,
    experience_level: str = 'beginner'
) -> dict:
    df = load_crops()
    crop = df[df['id'] == crop_id]

    if crop.empty:
        raise ValueError(f'Crop {crop_id} not found')

    crop = crop.iloc[0]

    yield_data  = estimate_yield(crop_id, system_type, area_sqft, experience_level)
    price       = crop['export_price_per_kg'] if target_market == 'export' else crop['local_price_per_kg']

    annual_revenue          = yield_data['annual_yield_kg'] * price
    annual_operating_cost   = monthly_operating_cost * 12
    annual_profit           = annual_revenue - annual_operating_cost
    breakeven_months        = (setup_cost / (annual_profit / 12)) if annual_profit > 0 else None

    return {
    'crop_name':                str(crop['name']),
    'annual_revenue':           round(float(annual_revenue), 2),
    'annual_operating_cost':    round(float(annual_operating_cost), 2),
    'annual_profit':            round(float(annual_profit), 2),
    'setup_cost':               round(float(setup_cost), 2),
    'breakeven_months':         round(float(breakeven_months), 1) if breakeven_months else 'N/A',
    'roi_percentage':           round(float((annual_profit / setup_cost) * 100), 1) if setup_cost > 0 else 0,
    'price_per_kg':             int(price),
    'target_market':            target_market
 }