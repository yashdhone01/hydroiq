import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY     = os.getenv('DATA_GOV_API_KEY')
RESOURCE_ID = '9ef84268-d588-465a-a308-a864a43d0070'
BASE_URL    = f'https://api.data.gov.in/resource/{RESOURCE_ID}'

# mapping our crop IDs to mandi commodity names
CROP_COMMODITY_MAP = {
    'basil':         'Basil Leaves',
    'mint':          'Mint',
    'lettuce':       'Lettuce',
    'spinach':       'Spinach',
    'kale':          'Kale',
    'cherry_tomato': 'Tomato',
    'cucumber':      'Cucumber',
    'strawberry':    'Strawberry'
}

def fetch_mandi_price(crop_id: str) -> dict:
    commodity = CROP_COMMODITY_MAP.get(crop_id)
    if not commodity:
        return {'error': f'No commodity mapping for {crop_id}'}

    try:
        params = {
            'api-key': API_KEY,
            'format':  'json',
            'limit':   10,
            'filters[commodity]': commodity
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        data     = response.json()

        records = data.get('records', [])
        if not records:
            return {'error': f'No data found for {commodity}', 'fallback': True}

        # extract modal prices and average them
        prices = []
        for r in records:
            try:
                # mandi prices are per quintal (100kg) — convert to per kg
                modal = float(r.get('modal_price', 0)) / 100
                if modal > 0:
                    prices.append(modal)
            except (ValueError, TypeError):
                continue

        if not prices:
            return {'error': 'Could not parse prices', 'fallback': True}

        avg_price = round(sum(prices) / len(prices), 2)

        return {
            'crop_id':        crop_id,
            'commodity':      commodity,
            'avg_price_per_kg': avg_price,
            'records_used':   len(prices),
            'source':         'data.gov.in Agmarknet',
            'live':           True
        }

    except Exception as e:
        return {'error': str(e), 'fallback': True}

def fetch_all_mandi_prices() -> dict:
    prices = {}
    for crop_id in CROP_COMMODITY_MAP:
        result = fetch_mandi_price(crop_id)
        if not result.get('fallback') and not result.get('error'):
            prices[crop_id] = result['avg_price_per_kg']
    return prices