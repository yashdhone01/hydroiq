import pytest
from app.models.yield_estimator import estimate_yield, calculate_roi


class TestEstimateYield:
    def test_basic_yield(self):
        result = estimate_yield(crop_id='basil', system_type='NFT', area_sqft=100)
        assert result['crop_name'] == 'Basil'
        assert result['yield_per_cycle_kg'] > 0
        assert result['annual_yield_kg'] > 0

    def test_experience_levels(self):
        beginner = estimate_yield('basil', 'NFT', 100, 'beginner')
        expert   = estimate_yield('basil', 'NFT', 100, 'expert')
        assert expert['yield_per_cycle_kg'] > beginner['yield_per_cycle_kg'], \
            "Expert should yield more than beginner"

    def test_system_multiplier_dwc(self):
        nft = estimate_yield('basil', 'NFT',   100, 'expert')
        dwc = estimate_yield('basil', 'DWC',   100, 'expert')
        assert dwc['yield_per_cycle_kg'] > nft['yield_per_cycle_kg'], \
            "DWC should yield more than NFT (15% boost)"

    def test_system_multiplier_kratky(self):
        nft    = estimate_yield('basil', 'NFT',    100, 'expert')
        kratky = estimate_yield('basil', 'Kratky', 100, 'expert')
        assert kratky['yield_per_cycle_kg'] < nft['yield_per_cycle_kg'], \
            "Kratky should yield less than NFT (15% reduction)"

    def test_area_scales_yield(self):
        small = estimate_yield('basil', 'NFT', 100,  'expert')
        large = estimate_yield('basil', 'NFT', 1000, 'expert')
        assert large['yield_per_cycle_kg'] == pytest.approx(
            small['yield_per_cycle_kg'] * 10, rel=0.01)

    def test_invalid_crop_raises(self):
        with pytest.raises(ValueError, match="not found"):
            estimate_yield('nonexistent', 'NFT', 100)

    def test_result_structure(self):
        result = estimate_yield('lettuce', 'DWC', 200, 'intermediate')
        required = ['crop_name', 'system_type', 'area_sqft', 'experience_level',
                     'yield_per_cycle_kg', 'cycles_per_year', 'annual_yield_kg',
                     'growth_days', 'system_efficiency', 'experience_efficiency']
        for key in required:
            assert key in result, f"Missing key: {key}"


class TestCalculateROI:
    def test_basic_roi(self):
        result = calculate_roi(
            crop_id='basil', system_type='NFT', area_sqft=500,
            target_market='export', setup_cost=50000,
            monthly_operating_cost=5000
        )
        assert result['crop_name'] == 'Basil'
        assert result['annual_revenue'] > 0
        assert 'breakeven_months' in result

    def test_export_higher_revenue_than_local(self):
        export_roi = calculate_roi(
            'basil', 'NFT', 500, 'export', 50000, 5000, 'expert')
        local_roi  = calculate_roi(
            'basil', 'NFT', 500, 'local',  50000, 5000, 'expert')
        assert export_roi['annual_revenue'] > local_roi['annual_revenue']

    def test_invalid_crop_raises(self):
        with pytest.raises(ValueError, match="not found"):
            calculate_roi('nonexistent', 'NFT', 500, 'local', 50000, 5000)

    def test_breakeven_with_loss(self):
        result = calculate_roi(
            crop_id='basil', system_type='NFT', area_sqft=10,
            target_market='local', setup_cost=500000,
            monthly_operating_cost=50000
        )
        # very high costs relative to tiny area → loss
        assert result['breakeven_months'] == 'N/A'

    def test_water_cost_zero_by_default(self):
        result = calculate_roi(
            'basil', 'NFT', 500, 'export', 50000, 5000)
        assert result['annual_water_cost'] == 0.0

    def test_water_cost_increases_operating_cost(self):
        without_water = calculate_roi(
            'basil', 'NFT', 500, 'export', 50000, 5000,
            water_cost_per_liter=0.0)
        with_water = calculate_roi(
            'basil', 'NFT', 500, 'export', 50000, 5000,
            water_cost_per_liter=0.5)
        assert with_water['annual_water_cost'] > 0
        assert with_water['annual_operating_cost'] > without_water['annual_operating_cost']
        assert with_water['annual_profit'] < without_water['annual_profit']

    def test_result_structure(self):
        result = calculate_roi(
            'mint', 'DWC', 300, 'local', 30000, 3000, 'intermediate')
        required = ['crop_name', 'annual_revenue', 'annual_operating_cost',
                     'annual_water_cost', 'annual_profit', 'setup_cost',
                     'breakeven_months', 'roi_percentage', 'price_per_kg',
                     'target_market']
        for key in required:
            assert key in result, f"Missing key: {key}"
