from fastapi import APIRouter, Query
from app.models.recommender import load_crops

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/intel")
def get_export_intel(
    crop_id: str = Query(None, description="Specific crop ID, or leave empty for all")
):
    df = load_crops()

    if crop_id:
        df = df[df['id'] == crop_id]
        if df.empty:
            return {"error": f"Crop {crop_id} not found"}

    result = []
    for _, row in df.iterrows():
        price_diff      = row['export_price_per_kg'] - row['local_price_per_kg']
        price_ratio     = round(row['export_price_per_kg'] / row['local_price_per_kg'], 1)

        result.append({
            "id":                   row['id'],
            "name":                 row['name'],
            "local_price_per_kg":   row['local_price_per_kg'],
            "export_price_per_kg":  row['export_price_per_kg'],
            "price_difference":     price_diff,
            "export_premium":       f"{price_ratio}x",
            "export_markets":       row['export_markets'],
            "best_for_export":      price_ratio >= 3.0
        })

    # sort by export premium
    result = sorted(result, key=lambda x: x['price_difference'], reverse=True)

    return {
        "count": len(result),
        "crops": result
    }

@router.get("/markets")
def get_markets():
    return {
        "markets": [
            {
                "name": "UAE",
                "demand": "High",
                "top_crops": ["Basil", "Lettuce", "Mint", "Cherry Tomato"],
                "notes": "Largest Indian hydroponic export market"
            },
            {
                "name": "EU",
                "demand": "High",
                "top_crops": ["Basil", "Kale", "Mint", "Strawberry"],
                "notes": "Requires GlobalGAP certification"
            },
            {
                "name": "UK",
                "demand": "Medium",
                "top_crops": ["Basil", "Spinach", "Cherry Tomato", "Kale"],
                "notes": "Post-Brexit import rules apply"
            },
            {
                "name": "Singapore",
                "demand": "Medium",
                "top_crops": ["Lettuce", "Cucumber", "Spinach"],
                "notes": "Premium pricing for pesticide-free produce"
            },
            {
                "name": "USA",
                "demand": "Growing",
                "top_crops": ["Mint", "Kale"],
                "notes": "High value but complex logistics"
            }
        ]
    }