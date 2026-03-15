import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def train_yield_model():
    np.random.seed(42)

    systems     = ['NFT', 'DWC', 'Kratky']
    crops       = ['basil', 'mint', 'lettuce', 'spinach', 'kale',
                   'cherry_tomato', 'cucumber', 'strawberry']
    experiences = ['beginner', 'intermediate', 'expert']

    base_yields = {
        ('basil','NFT'):0.45,('basil','DWC'):0.52,('basil','Kratky'):0.38,
        ('mint','NFT'):0.40,('mint','DWC'):0.46,('mint','Kratky'):0.34,
        ('lettuce','NFT'):0.60,('lettuce','DWC'):0.69,('lettuce','Kratky'):0.45,
        ('spinach','NFT'):0.50,('spinach','DWC'):0.57,('spinach','Kratky'):0.42,
        ('kale','NFT'):0.55,('kale','DWC'):0.63,('kale','Kratky'):0.46,
        ('cherry_tomato','NFT'):1.20,('cherry_tomato','DWC'):1.38,('cherry_tomato','Kratky'):0.90,
        ('cucumber','NFT'):1.50,('cucumber','DWC'):1.72,('cucumber','Kratky'):1.20,
        ('strawberry','NFT'):0.80,('strawberry','DWC'):0.92,('strawberry','Kratky'):0.65,
    }
    exp_mult = {'beginner':0.70,'intermediate':0.90,'expert':1.00}

    records = []
    for _ in range(2000):
        crop   = np.random.choice(crops)
        system = np.random.choice(systems)
        area   = np.random.uniform(50, 2000)
        exp    = np.random.choice(experiences)
        base   = base_yields.get((crop, system), 0.5)
        noise  = np.random.normal(1.0, 0.08)
        records.append({
            'crop': crop, 'system': system,
            'area_sqft': area, 'experience': exp,
            'yield_per_sqft': base * exp_mult[exp] * noise
        })

    df = pd.DataFrame(records)
    le_crop   = LabelEncoder()
    le_system = LabelEncoder()
    le_exp    = LabelEncoder()
    df['crop_enc']   = le_crop.fit_transform(df['crop'])
    df['system_enc'] = le_system.fit_transform(df['system'])
    df['exp_enc']    = le_exp.fit_transform(df['experience'])

    X = df[['crop_enc','system_enc','area_sqft','exp_enc']]
    y = df['yield_per_sqft']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    print(f"MAE : {mean_absolute_error(y_test, model.predict(X_test)):.4f}")
    print(f"R²  : {r2_score(y_test, model.predict(X_test)):.4f}")

    os.makedirs(os.path.join(os.path.dirname(__file__), 'saved'), exist_ok=True)
    save_dir = os.path.join(os.path.dirname(__file__), 'saved')
    joblib.dump(model,    os.path.join(save_dir, 'yield_model.pkl'))
    joblib.dump(le_crop,  os.path.join(save_dir, 'le_crop.pkl'))
    joblib.dump(le_system,os.path.join(save_dir, 'le_system.pkl'))
    joblib.dump(le_exp,   os.path.join(save_dir, 'le_exp.pkl'))
    print("Model saved!")

if __name__ == '__main__':
    train_yield_model()