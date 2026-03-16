"""
Train a price prediction model using historical commodity price data.

Model: GradientBoostingRegressor
Features: crop, region, month, quarter, historical avg, volatility, trend
Target: modal_price per kg
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

from app.services.data_pipeline import load_and_clean


SAVE_DIR = os.path.join(os.path.dirname(__file__), 'saved')


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add rolling/derived features for price prediction."""
    df = df.sort_values(['crop_id', 'date']).copy()

    features = []
    for crop_id, group in df.groupby('crop_id'):
        g = group.copy()

        # rolling averages (window sizes in number of records, not days)
        g['rolling_avg_30']  = g['modal_price'].rolling(window=10, min_periods=1).mean()
        g['rolling_avg_90']  = g['modal_price'].rolling(window=30, min_periods=1).mean()

        # price volatility (rolling std)
        g['volatility']      = g['modal_price'].rolling(window=10, min_periods=1).std().fillna(0)

        # price trend (pct change over window)
        g['price_trend']     = g['modal_price'].pct_change(periods=10).fillna(0)

        # min-max spread as percentage
        g['price_spread']    = ((g['max_price'] - g['min_price']) / g['modal_price']).fillna(0)

        features.append(g)

    return pd.concat(features, ignore_index=True)


def train_price_model():
    """Train and save the price prediction model."""
    print("Loading data for price model training...")
    df = load_and_clean()
    df = _engineer_features(df)

    # encode categoricals
    le_crop   = LabelEncoder()
    le_region = LabelEncoder()

    df['crop_enc']   = le_crop.fit_transform(df['crop_id'])
    df['region_enc'] = le_region.fit_transform(df['region'])

    feature_cols = [
        'crop_enc', 'region_enc', 'month', 'quarter',
        'rolling_avg_30', 'rolling_avg_90', 'volatility',
        'price_trend', 'price_spread'
    ]

    X = df[feature_cols].fillna(0)
    y = df['modal_price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2  = r2_score(y_test, preds)
    print(f"Price Model — MAE: ₹{mae:.2f}/kg  |  R²: {r2:.4f}")

    # save model and encoders
    os.makedirs(SAVE_DIR, exist_ok=True)
    joblib.dump(model,     os.path.join(SAVE_DIR, 'price_model.pkl'))
    joblib.dump(le_crop,   os.path.join(SAVE_DIR, 'price_le_crop.pkl'))
    joblib.dump(le_region, os.path.join(SAVE_DIR, 'price_le_region.pkl'))

    # save feature importance for interpretability
    importance = dict(zip(feature_cols, model.feature_importances_))
    joblib.dump(importance, os.path.join(SAVE_DIR, 'price_feature_importance.pkl'))

    # save model metrics
    joblib.dump({'mae': mae, 'r2': r2}, os.path.join(SAVE_DIR, 'price_metrics.pkl'))

    print("Price model saved!")
    return {'mae': mae, 'r2': r2}


if __name__ == '__main__':
    train_price_model()
