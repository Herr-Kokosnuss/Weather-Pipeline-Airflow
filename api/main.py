import os
import sys
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import CITIES, get_latest_prediction, fetch_weather_data

app = FastAPI(title="Weather Prediction API", 
              description="API for weather temperature predictions for German cities",
              version="1.0.0")

class PredictionResponse(BaseModel):
    city: str
    current_temperature: float
    current_humidity: float
    prediction_date: str
    predicted_temperature: float
    last_updated: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Prediction API", 
            "available_cities": CITIES,
            "endpoints": ["/predictions", "/predictions/{city}"]}

@app.get("/predictions", response_model=List[PredictionResponse])
def get_all_predictions():
    """Get predictions for all cities"""
    results = []
    
    for city in CITIES:
        try:
            result = get_city_prediction(city)
            results.append(result)
        except HTTPException:
            # Skip cities with errors
            pass
    
    if not results:
        raise HTTPException(status_code=404, detail="No predictions available")
    
    return results

@app.get("/predictions/{city}", response_model=PredictionResponse)
def get_prediction(city: str):
    """Get prediction for a specific city"""
    if city not in CITIES:
        raise HTTPException(status_code=404, detail=f"City not found. Available cities: {', '.join(CITIES)}")
    
    return get_city_prediction(city)

def get_city_prediction(city: str) -> PredictionResponse:
    """Helper function to get prediction for a city"""
    # Get current weather data
    current_data = fetch_weather_data(city)
    if not current_data:
        raise HTTPException(status_code=503, detail=f"Could not fetch current weather data for {city}")
    
    # Get latest prediction from database
    prediction = get_latest_prediction(city)
    if not prediction:
        raise HTTPException(status_code=404, detail=f"No prediction available for {city}")
    
    return PredictionResponse(
        city=city,
        current_temperature=current_data['temperature'],
        current_humidity=current_data['humidity'],
        prediction_date=prediction['prediction_date'].strftime("%Y-%m-%d"),
        predicted_temperature=prediction['predicted_temperature'],
        last_updated=prediction['created_at'].strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 