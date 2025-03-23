import os
import sys
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import pytz
from typing import List, Optional
from api.chatbot import get_chat_response  # Fixed import

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.utils import CITIES, get_latest_prediction, fetch_weather_data, get_db_connection

# Define German timezone
german_tz = pytz.timezone('Europe/Berlin')

app = FastAPI(title="Weather Prediction API", 
              description="API for weather temperature predictions for German cities",
              version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class HistoricalReading(BaseModel):
    date: str
    temperature: float
    humidity: float

class PredictionResponse(BaseModel):
    city: str
    current_temperature: float
    current_humidity: float
    prediction_date: str
    predicted_temperature: float
    last_updated: str
    historical_data: List[HistoricalReading]

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

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
    
    # Convert UTC timestamp to German time
    utc_time = current_data['timestamp'].replace(tzinfo=pytz.UTC)
    german_time = utc_time.astimezone(german_tz)
    
    # Get latest prediction from database
    prediction = get_latest_prediction(city)
    if not prediction:
        raise HTTPException(status_code=404, detail=f"No prediction available for {city}")
    
    # Get historical data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        WITH RankedData AS (
            SELECT DISTINCT ON (DATE(timestamp)) 
                timestamp,
                temperature,
                humidity
            FROM weather_data
            WHERE city = %s
            ORDER BY DATE(timestamp) DESC, timestamp DESC
        )
        SELECT * FROM RankedData
        LIMIT 5
        """,
        (city,)
    )
    historical_data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format historical data
    historical_readings = []
    for reading in historical_data:
        # Convert historical timestamps to German time
        utc_reading_time = reading[0].replace(tzinfo=pytz.UTC)
        german_reading_time = utc_reading_time.astimezone(german_tz)
        historical_readings.append(HistoricalReading(
            date=german_reading_time.strftime("%Y-%m-%d 12:00 PM"),
            temperature=reading[1],
            humidity=reading[2]
        ))
    
    # Sort historical readings by date (oldest first)
    historical_readings.sort(key=lambda x: x.date)
    
    return PredictionResponse(
        city=city,
        current_temperature=current_data['temperature'],
        current_humidity=current_data['humidity'],
        prediction_date=prediction['prediction_date'].strftime("%Y-%m-%d"),
        predicted_temperature=prediction['predicted_temperature'],
        last_updated=german_time.strftime("%Y-%m-%d %H:%M:%S"),
        historical_data=historical_readings
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Process a chat message and return the response"""
    try:
        response = await get_chat_response(message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 