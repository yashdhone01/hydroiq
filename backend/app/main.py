from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import crops, export, roi
from app.services.agmarknet_service import fetch_all_mandi_prices

app = FastAPI(
    title="HydroIQ API",
    description="Crop intelligence platform for hydroponic growers",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# live price cache — updated on startup
app.state.live_prices = {}

@app.on_event("startup")
async def startup_event():
    print("Fetching live mandi prices...")
    app.state.live_prices = fetch_all_mandi_prices()
    print(f"Live prices loaded: {app.state.live_prices}")

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

@app.get("/debug/prices")
def debug_prices():
    from app.services.agmarknet_service import fetch_mandi_price
    return {
        "basil": fetch_mandi_price('basil'),
        "mint":  fetch_mandi_price('mint'),
        "spinach": fetch_mandi_price('spinach'),
        "cherry_tomato": fetch_mandi_price('cherry_tomato')
    }