import os
import joblib
import numpy as np
import json
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'saved')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'crops.json')

def load_model():
    model     = joblib.load(os.path.join(MODEL_DIR, 'yield_model.pkl'))
    le_crop   = joblib.load(os.path.join(MODEL_DIR, 'le_crop.pkl'))
    le_system = joblib.load(os.path.join(MODEL_DIR, 'le_system.pkl'))
    le_exp    = joblib.load(os.path.join(MODEL_DIR, 'le_exp.pkl'))
    return model, le_crop, le_system, le_exp

def load_crops() -> pd.DataFrame:
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['crops'])

def estimate_yield(
    crop_id:          str,
    system_type:      str,
    area_sqft:        float,
    experience_level: str = 'beginner'
) -> dict:
    try:
        model, le_crop, le_system, le_exp = load_model()
    except Exception:
        return {'error': 'Model not found. Run train_yield_model.py first.'}

    df   = load_crops()
    crop = df[df['id'] == crop_id]
    if crop.empty:
        return {'error': f'Crop {crop_id} not found'}
    crop = crop.iloc[0]

    try:
        crop_enc   = le_crop.transform([crop_id])[0]
        system_enc = le_system.transform([system_type])[0]
        exp_enc    = le_exp.transform([experience_level])[0]
    except ValueError as e:
        return {'error': f'Invalid input: {str(e)}'}

    X = np.array([[crop_enc, system_enc, float(area_sqft), exp_enc]])
    yield_per_sqft  = float(model.predict(X)[0])
    yield_per_cycle = round(yield_per_sqft * area_sqft, 2)
    annual_yield    = round(yield_per_cycle * int(crop['cycles_per_year']), 2)

    return {
        'crop_name':            str(crop['name']),
        'system_type':          system_type,
        'area_sqft':            float(area_sqft),
        'experience_level':     experience_level,
        'yield_per_sqft':       round(yield_per_sqft, 4),
        'yield_per_cycle_kg':   yield_per_cycle,
        'cycles_per_year':      int(crop['cycles_per_year']),
        'annual_yield_kg':      annual_yield,
        'growth_days':          int(crop['growth_days']),
        'model':                'GradientBoostingRegressor',
        'r2_score':             0.9644
    }

def calculate_roi(
    crop_id:                str,
    system_type:            str,
    area_sqft:              float,
    target_market:          str,
    setup_cost:             float,
    monthly_operating_cost: float,
    experience_level:       str = 'beginner'
) -> dict:
    df   = load_crops()
    crop = df[df['id'] == crop_id]
    if crop.empty:
        return {'error': f'Crop {crop_id} not found'}
    crop = crop.iloc[0]

    yield_data = estimate_yield(crop_id, system_type, area_sqft, experience_level)
    if 'error' in yield_data:
        return yield_data

    price = float(crop['export_price_per_kg']) if target_market == 'export' \
            else float(crop['local_price_per_kg'])

    annual_revenue       = round(yield_data['annual_yield_kg'] * price, 2)
    annual_operating     = round(monthly_operating_cost * 12, 2)
    annual_profit        = round(annual_revenue - annual_operating, 2)
    breakeven_months     = round(setup_cost / (annual_profit / 12), 1) \
                           if annual_profit > 0 else None

    return {
        'crop_name':             str(crop['name']),
        'annual_revenue':        annual_revenue,
        'annual_operating_cost': annual_operating,
        'annual_profit':         annual_profit,
        'setup_cost':            float(setup_cost),
        'breakeven_months':      breakeven_months if breakeven_months else 'N/A',
        'roi_percentage':        round((annual_profit / setup_cost) * 100, 1) \
                                 if setup_cost > 0 else 0,
        'price_per_kg':          int(price),
        'target_market':         target_market,
        'model':                 'GradientBoostingRegressor',
        'r2_score':              0.9644
    }