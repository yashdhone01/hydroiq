"""
Data pipeline for loading and cleaning the Kaggle Agri Commodity dataset.

If the real dataset (agridata.csv) is not present, generates a realistic
synthetic dataset so the models can train immediately.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR  = os.path.join(os.path.dirname(__file__), '..', 'data')
CSV_PATH  = os.path.join(DATA_DIR, 'agridata.csv')
CLEAN_PKL = os.path.join(DATA_DIR, 'agridata_clean.pkl')

# mapping from our crop IDs to Agmarknet commodity names
CROP_COMMODITY_MAP = {
    'basil':         ['Basil Leaves', 'Basil'],
    'mint':          ['Mint', 'Mentha Oil'],
    'lettuce':       ['Lettuce'],
    'spinach':       ['Spinach', 'Palak'],
    'kale':          ['Kale'],
    'cherry_tomato': ['Tomato', 'Cherry Tomato'],
    'cucumber':      ['Cucumber', 'Cucumber (Kheera)'],
    'strawberry':    ['Strawberry'],
}

# reverse lookup: commodity name → crop_id
_COMMODITY_TO_CROP = {}
for crop_id, names in CROP_COMMODITY_MAP.items():
    for name in names:
        _COMMODITY_TO_CROP[name.lower()] = crop_id

REGIONS = ['North', 'South', 'East', 'West']


def _generate_synthetic_data() -> pd.DataFrame:
    """Generate realistic synthetic price data when real CSV is unavailable."""
    np.random.seed(42)

    # base prices per kg (realistic Indian market ranges)
    base_prices = {
        'basil':         {'mean': 150, 'std': 40},
        'mint':          {'mean': 200, 'std': 50},
        'lettuce':       {'mean': 80,  'std': 20},
        'spinach':       {'mean': 60,  'std': 15},
        'kale':          {'mean': 180, 'std': 45},
        'cherry_tomato': {'mean': 120, 'std': 35},
        'cucumber':      {'mean': 40,  'std': 12},
        'strawberry':    {'mean': 300, 'std': 80},
    }

    # seasonality patterns (multiplier by quarter)
    seasonality = {
        'basil':         [1.0, 1.1, 0.9, 1.05],
        'mint':          [1.1, 1.2, 0.85, 0.95],
        'lettuce':       [0.9, 0.85, 1.1, 1.15],
        'spinach':       [1.15, 0.9, 0.85, 1.1],
        'kale':          [1.1, 0.9, 0.95, 1.05],
        'cherry_tomato': [0.85, 1.15, 1.1, 0.9],
        'cucumber':      [0.9, 1.2, 1.1, 0.8],
        'strawberry':    [1.3, 0.8, 0.7, 1.2],
    }

    records = []
    start_date = datetime(2019, 1, 1)
    num_days = 365 * 3  # 3 years of data

    for day_offset in range(0, num_days, 3):  # every 3 days
        date = start_date + timedelta(days=day_offset)
        quarter = (date.month - 1) // 3

        for crop_id, prices in base_prices.items():
            season_mult = seasonality[crop_id][quarter]
            # yearly inflation trend (3-5% per year)
            year_mult = 1 + 0.04 * (day_offset / 365)

            base = prices['mean'] * season_mult * year_mult
            noise = np.random.normal(0, prices['std'] * 0.3)
            modal = max(5, base + noise)

            for region in REGIONS:
                # regional price variation (±10%)
                region_mult = 1.0 + np.random.uniform(-0.10, 0.10)
                r_modal = round(modal * region_mult, 2)
                r_min   = round(r_modal * np.random.uniform(0.75, 0.90), 2)
                r_max   = round(r_modal * np.random.uniform(1.10, 1.30), 2)

                commodity = CROP_COMMODITY_MAP[crop_id][0]
                records.append({
                    'commodity':   commodity,
                    'state':       f'{region}_State',
                    'district':    f'{region}_District',
                    'market':      f'{region}_Market',
                    'min_price':   r_min,
                    'max_price':   r_max,
                    'modal_price': r_modal,
                    'region':      region,
                    'date':        date.strftime('%Y-%m-%d'),
                    'crop_id':     crop_id,
                })

    return pd.DataFrame(records)


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names from various Kaggle CSV formats."""
    col_map = {}
    for col in df.columns:
        lower = col.strip().lower().replace(' ', '_')
        if 'commodity' in lower and 'name' in lower:
            col_map[col] = 'commodity'
        elif lower == 'commodity':
            col_map[col] = 'commodity'
        elif 'min' in lower and 'price' in lower:
            col_map[col] = 'min_price'
        elif 'max' in lower and 'price' in lower:
            col_map[col] = 'max_price'
        elif 'modal' in lower and 'price' in lower:
            col_map[col] = 'modal_price'
        elif lower == 'state':
            col_map[col] = 'state'
        elif lower == 'district':
            col_map[col] = 'district'
        elif lower == 'market':
            col_map[col] = 'market'
        elif lower == 'region':
            col_map[col] = 'region'
        elif 'date' in lower:
            col_map[col] = 'date'

    df = df.rename(columns=col_map)
    return df


def _map_crop_id(commodity_name: str) -> str:
    """Map commodity name to our crop_id."""
    if pd.isna(commodity_name):
        return None
    return _COMMODITY_TO_CROP.get(commodity_name.strip().lower())


def load_and_clean(force_reload: bool = False) -> pd.DataFrame:
    """
    Load, clean, and enrich the commodity price data.
    Returns a DataFrame with columns:
    [crop_id, commodity, date, min_price, max_price, modal_price,
     region, state, month, quarter, year]
    """
    # use cached version if available
    if not force_reload and os.path.exists(CLEAN_PKL):
        return pd.read_pickle(CLEAN_PKL)

    # load real CSV or generate synthetic
    if os.path.exists(CSV_PATH):
        print(f"Loading real dataset from {CSV_PATH}...")
        df = pd.read_csv(CSV_PATH, low_memory=False)
        df = _standardize_columns(df)

        # map commodities to our crop IDs
        df['crop_id'] = df['commodity'].apply(_map_crop_id)
        df = df.dropna(subset=['crop_id'])
    else:
        print("Real dataset not found — generating synthetic price data...")
        df = _generate_synthetic_data()

    # parse dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # ensure numeric prices
    for col in ['min_price', 'max_price', 'modal_price']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['modal_price'])
    df = df[df['modal_price'] > 0]

    # extract date features
    df['month']   = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['year']    = df['date'].dt.year

    # assign region if missing (based on state heuristics)
    if 'region' not in df.columns or df['region'].isna().all():
        df['region'] = 'National'

    # sort by date
    df = df.sort_values('date').reset_index(drop=True)

    # cache cleaned data
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_pickle(CLEAN_PKL)
    print(f"Cleaned data: {len(df)} records for {df['crop_id'].nunique()} crops")

    return df


def get_historical_avg_prices() -> dict:
    """Returns {crop_id: avg_modal_price_per_kg} from historical data."""
    df = load_and_clean()
    return df.groupby('crop_id')['modal_price'].mean().round(2).to_dict()


def get_price_stats(crop_id: str) -> dict:
    """Detailed price statistics for a specific crop."""
    df = load_and_clean()
    crop_df = df[df['crop_id'] == crop_id]

    if crop_df.empty:
        return {'error': f'No data for {crop_id}'}

    return {
        'crop_id':       crop_id,
        'records':       len(crop_df),
        'avg_price':     round(crop_df['modal_price'].mean(), 2),
        'min_price':     round(crop_df['min_price'].min(), 2),
        'max_price':     round(crop_df['max_price'].max(), 2),
        'std_dev':       round(crop_df['modal_price'].std(), 2),
        'date_range':    f"{crop_df['date'].min().date()} to {crop_df['date'].max().date()}",
        'by_quarter':    crop_df.groupby('quarter')['modal_price'].mean().round(2).to_dict(),
    }
