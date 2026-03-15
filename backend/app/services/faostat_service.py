import requests

# FAOSTAT crop codes for our crops
FAOSTAT_CROP_MAP = {
    'basil':         {'code': 'basil',    'fao_name': 'Basil',         'avg_yield_kg_ha': 8000},
    'mint':          {'code': 'mint',     'fao_name': 'Peppermint',    'avg_yield_kg_ha': 7500},
    'lettuce':       {'code': 'lettuce',  'fao_name': 'Lettuce',       'avg_yield_kg_ha': 22000},
    'spinach':       {'code': 'spinach',  'fao_name': 'Spinach',       'avg_yield_kg_ha': 18000},
    'kale':          {'code': 'kale',     'fao_name': 'Kale',          'avg_yield_kg_ha': 15000},
    'cherry_tomato': {'code': 'tomato',   'fao_name': 'Tomatoes',      'avg_yield_kg_ha': 38000},
    'cucumber':      {'code': 'cucumber', 'fao_name': 'Cucumbers',     'avg_yield_kg_ha': 32000},
    'strawberry':    {'code': 'straw',    'fao_name': 'Strawberries',  'avg_yield_kg_ha': 12000},
}

# hydroponic multiplier — hydroponics yields 2-5x vs soil
HYDROPONIC_MULTIPLIER = 3.0
SQFT_PER_HECTARE      = 107639.0

def get_yield_benchmark(crop_id: str) -> dict:
    crop = FAOSTAT_CROP_MAP.get(crop_id)
    if not crop:
        return {'error': f'No FAO data for {crop_id}'}

    try:
        # try live FAOSTAT API
        url    = 'https://fenixservices.fao.org/faostat/api/v1/en/data/QCL'
        params = {
            'item':    crop['fao_name'],
            'element': 'Yield',
            'area':    'India',
            'year':    '2022',
            'output_type': 'json'
        }
        response = requests.get(url, params=params, timeout=8)
        data     = response.json()
        records  = data.get('data', [])

        if records:
            yield_kg_ha = float(records[0].get('Value', crop['avg_yield_kg_ha']))
        else:
            yield_kg_ha = crop['avg_yield_kg_ha']

    except Exception:
        # fallback to research-based values
        yield_kg_ha = crop['avg_yield_kg_ha']

    # convert to kg/sqft for hydroponic context
    soil_yield_sqft  = yield_kg_ha / SQFT_PER_HECTARE
    hydro_yield_sqft = round(soil_yield_sqft * HYDROPONIC_MULTIPLIER, 4)

    return {
        'crop_id':              crop_id,
        'fao_name':             crop['fao_name'],
        'soil_yield_kg_sqft':   round(soil_yield_sqft, 4),
        'hydro_yield_kg_sqft':  hydro_yield_sqft,
        'hydroponic_multiplier': HYDROPONIC_MULTIPLIER,
        'source':               'FAOSTAT'
    }

import requests

FAOSTAT_CROP_MAP = {
    'basil':         {'code': 'basil',    'fao_name': 'Basil',         'avg_yield_kg_ha': 8000},
    'mint':          {'code': 'mint',     'fao_name': 'Peppermint',    'avg_yield_kg_ha': 7500},
    'lettuce':       {'code': 'lettuce',  'fao_name': 'Lettuce',       'avg_yield_kg_ha': 22000},
    'spinach':       {'code': 'spinach',  'fao_name': 'Spinach',       'avg_yield_kg_ha': 18000},
    'kale':          {'code': 'kale',     'fao_name': 'Kale',          'avg_yield_kg_ha': 15000},
    'cherry_tomato': {'code': 'tomato',   'fao_name': 'Tomatoes',      'avg_yield_kg_ha': 38000},
    'cucumber':      {'code': 'cucumber', 'fao_name': 'Cucumbers',     'avg_yield_kg_ha': 32000},
    'strawberry':    {'code': 'straw',    'fao_name': 'Strawberries',  'avg_yield_kg_ha': 12000},
}

HYDROPONIC_MULTIPLIER = 3.0
SQFT_PER_HECTARE      = 107639.0

def get_yield_benchmark(crop_id: str) -> dict:
    crop = FAOSTAT_CROP_MAP.get(crop_id)
    if not crop:
        return {'error': f'No FAO data for {crop_id}'}

    try:
        url    = 'https://fenixservices.fao.org/faostat/api/v1/en/data/QCL'
        params = {
            'item':        crop['fao_name'],
            'element':     'Yield',
            'area':        'India',
            'year':        '2022',
            'output_type': 'json'
        }
        response    = requests.get(url, params=params, timeout=8)
        data        = response.json()
        records     = data.get('data', [])
        yield_kg_ha = float(records[0].get('Value', crop['avg_yield_kg_ha'])) if records else crop['avg_yield_kg_ha']
    except Exception:
        yield_kg_ha = crop['avg_yield_kg_ha']

    soil_yield_sqft  = yield_kg_ha / SQFT_PER_HECTARE
    hydro_yield_sqft = round(soil_yield_sqft * HYDROPONIC_MULTIPLIER, 4)

    return {
        'crop_id':               crop_id,
        'fao_name':              crop['fao_name'],
        'soil_yield_kg_sqft':    round(soil_yield_sqft, 4),
        'hydro_yield_kg_sqft':   hydro_yield_sqft,
        'hydroponic_multiplier': HYDROPONIC_MULTIPLIER,
        'source':                'FAOSTAT'
    }

def get_all_benchmarks() -> dict:
    fallbacks = {
        'basil': 0.45, 'mint': 0.40, 'lettuce': 0.60,
        'spinach': 0.50, 'kale': 0.55, 'cherry_tomato': 1.20,
        'cucumber': 1.50, 'strawberry': 0.80
    }
    benchmarks = {}
    for crop_id in FAOSTAT_CROP_MAP:
        result = get_yield_benchmark(crop_id)
        benchmarks[crop_id] = result.get('hydro_yield_kg_sqft', fallbacks.get(crop_id, 0.5))
    return benchmarks