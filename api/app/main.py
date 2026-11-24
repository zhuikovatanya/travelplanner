from fastapi import FastAPI
from .routers.travel import router as travel_router

app = FastAPI(
    title="TravelPlanner API",
    description="REST API for planning trips, destinations and daily itineraries.",
    version="1.0.0",
)

app.include_router(travel_router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to TravelPlanner API", "docs": "/docs"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
