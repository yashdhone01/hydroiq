import pytest
from app.models.recommender import load_crops, recommend_crops


class TestLoadCrops:
    def test_returns_dataframe(self):
        df = load_crops()
        assert len(df) > 0, "Should load at least one crop"

    def test_has_required_columns(self):
        df = load_crops()
        required = ['id', 'name', 'systems', 'growth_days', 'yield_per_sqft_kg',
                     'local_price_per_kg', 'export_price_per_kg', 'cycles_per_year']
        for col in required:
            assert col in df.columns, f"Missing column: {col}"

    def test_all_crop_ids_unique(self):
        df = load_crops()
        assert df['id'].is_unique, "Crop IDs should be unique"


class TestRecommendCrops:
    def test_filters_by_system_type(self):
        results = recommend_crops(system_type='Kratky', area_sqft=100,
                                  target_market='local', budget=50000)
        # Kratky-compatible crops: basil, spinach, mint
        for crop in results:
            assert 'Kratky' in load_crops()[load_crops()['id'] == crop['id']]['systems'].iloc[0]

    def test_returns_empty_for_invalid_system(self):
        results = recommend_crops(system_type='InvalidSystem', area_sqft=100,
                                  target_market='local', budget=50000)
        assert results == []

    def test_respects_top_n(self):
        results = recommend_crops(system_type='NFT', area_sqft=100,
                                  target_market='local', budget=50000, top_n=2)
        assert len(results) <= 2

    def test_results_sorted_by_roi_score(self):
        results = recommend_crops(system_type='NFT', area_sqft=500,
                                  target_market='export', budget=100000, top_n=5)
        scores = [r['roi_score'] for r in results]
        assert scores == sorted(scores, reverse=True), "Should be sorted by ROI descending"

    def test_export_uses_export_price(self):
        results = recommend_crops(system_type='NFT', area_sqft=100,
                                  target_market='export', budget=50000)
        df = load_crops()
        for crop in results:
            row = df[df['id'] == crop['id']].iloc[0]
            assert crop['price_per_kg'] == round(float(row['export_price_per_kg']), 2)

    def test_local_uses_local_price(self):
        results = recommend_crops(system_type='NFT', area_sqft=100,
                                  target_market='local', budget=50000)
        df = load_crops()
        for crop in results:
            row = df[df['id'] == crop['id']].iloc[0]
            assert crop['price_per_kg'] == round(float(row['local_price_per_kg']), 2)

    def test_live_price_override(self):
        live_prices = {'basil': 999.0}
        results = recommend_crops(system_type='NFT', area_sqft=100,
                                  target_market='local', budget=50000,
                                  live_prices=live_prices)
        basil = next((r for r in results if r['id'] == 'basil'), None)
        if basil:
            assert basil['local_price_per_kg'] == 999.0
            assert basil['price_source'] == 'live'

    def test_result_structure(self):
        results = recommend_crops(system_type='NFT', area_sqft=100,
                                  target_market='local', budget=50000, top_n=1)
        assert len(results) >= 1
        crop = results[0]
        required_keys = ['id', 'name', 'difficulty', 'growth_days', 'cycles_per_year',
                         'yield_per_cycle_kg', 'revenue_per_cycle', 'annual_revenue',
                         'price_per_kg', 'roi_score', 'price_source']
        for key in required_keys:
            assert key in crop, f"Missing key: {key}"
