from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import crops, export, roi

app = FastAPI(
    title="HydroIQ API",
    description="Crop intelligence platform for hydroponic growers",
    version="1.0.0"
)

# CORS — allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(crops.router)
app.include_router(export.router)
app.include_router(roi.router)

@app.get("/")
def root():
    return {
        "name":    "HydroIQ API",
        "version": "1.0.0",
        "docs":    "/docs"
    }

@app.get("/health")
def health():
    return {"status": "running"}