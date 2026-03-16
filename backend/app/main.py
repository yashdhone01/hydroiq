from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import crops, export, roi
from app.services.agmarknet_service import fetch_all_mandi_prices

@asynccontextmanager
async def lifespan(app: FastAPI):
    # — startup —
    import os

    # env var check
    if not os.getenv('DATA_GOV_API_KEY'):
        print("⚠️  WARNING: DATA_GOV_API_KEY not set — live mandi prices will be unavailable")

    # train ML model if not cached
    model_path = os.path.join('app', 'models', 'saved', 'yield_model.pkl')
    if not os.path.exists(model_path):
        try:
            print("Training yield model...")
            from app.models.train_yield_model import train_yield_model
            train_yield_model()
        except Exception as e:
            print(f"⚠️  Model training failed: {e} — yield predictions may be unavailable")

    # fetch live prices
    print("Fetching live mandi prices...")
    app.state.live_prices = fetch_all_mandi_prices()
    print(f"Live prices loaded: {len(app.state.live_prices)} crops")

    yield
    # — shutdown (nothing to clean up) —

app = FastAPI(
    title="HydroIQ API",
    description="Crop intelligence platform for hydroponic growers",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crops.router)
app.include_router(export.router)
app.include_router(roi.router)

@app.get("/")
def root():
    return {
        "name":        "HydroIQ API",
        "version":     "2.0.0",
        "docs":        "/docs",
        "live_prices": app.state.live_prices
    }

@app.get("/health")
def health():
    return {
        "status":      "running",
        "live_prices": len(app.state.live_prices) > 0
    }

@app.get("/prices/live")
def get_live_prices():
    return {
        "source": "data.gov.in Agmarknet",
        "prices": app.state.live_prices
    }

@app.post("/prices/refresh")
def refresh_prices():
    app.state.live_prices = fetch_all_mandi_prices()
    return {
        "status":  "refreshed",
        "source":  "data.gov.in Agmarknet",
        "count":   len(app.state.live_prices),
        "prices":  app.state.live_prices
    }

@app.get("/debug/prices")
def debug_prices():
    from app.services.agmarknet_service import fetch_mandi_price
    return {
        "basil": fetch_mandi_price('basil'),
        "mint":  fetch_mandi_price('mint'),
        "spinach": fetch_mandi_price('spinach'),
        "cherry_tomato": fetch_mandi_price('cherry_tomato')
    }