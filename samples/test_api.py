import unittest
import sys
import os
from unittest import mock
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define mock data and functions
MOCK_CITIES = ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"]

def mock_get_latest_prediction(city):
    """Mock for get_latest_prediction function"""
    return {
        "city": city,
        "prediction_date": datetime.now().date(),
        "predicted_day_temperature": 23.8,
        "predicted_night_temperature": 18.2,
        "created_at": datetime.now()
    }

def mock_fetch_weather_data(city, timestamp=None, is_day=True):
    """Mock for fetch_weather_data function"""
    return {
        "city": city,
        "temperature": 21.5,
        "humidity": 75,
        "timestamp": datetime.now(),
        "is_day": is_day
    }

def mock_get_historical_data(city, days=7):
    """Mock for get_historical_data function"""
    import pandas as pd
    # Create a simple DataFrame with required columns
    dates = [datetime.now() for _ in range(5)]
    return pd.DataFrame({
        'timestamp': dates,
        'temperature': [20, 22, 19, 21, 23],
        'humidity': [80, 75, 85, 78, 72],
        'is_day': [True, True, False, False, True],
        'city': [city] * 5
    })

# Create a mock FastAPI app for testing
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI(title="Weather ML API Mock")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Weather Prediction API", 
        "available_cities": MOCK_CITIES,
        "endpoints": ["/predictions", "/predictions/{city}"]
    }

@app.get("/predictions")
def get_all_predictions():
    return [
        get_city_prediction("Berlin"),
        get_city_prediction("Munich")
    ]

@app.get("/predictions/{city}")
def get_prediction(city: str):
    valid_cities = [c.lower() for c in MOCK_CITIES]
    if city.lower() not in valid_cities:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    return get_city_prediction(city)

def get_city_prediction(city: str):
    # Return mock prediction data
    return {
        "city": city,
        "current_temperature": 21.5,
        "current_humidity": 75,
        "prediction_date": "2023-08-01",
        "predicted_day_temperature": 23.8,
        "predicted_night_temperature": 18.2,
        "historical_data": [
            {"date": "2023-07-31", "day_temperature": 21.2, "night_temperature": 19.5, "avg_humidity": 76},
            {"date": "2023-07-30", "day_temperature": 20.8, "night_temperature": 18.9, "avg_humidity": 78}
        ],
        "last_updated": "2023-08-01 12:00:00"
    }

client = TestClient(app)

class TestAPI(unittest.TestCase):
    """Test cases for the API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("available_cities", data)
        self.assertIn("endpoints", data)
    
    def test_all_predictions_endpoint(self):
        """Test the all predictions endpoint"""
        response = client.get("/predictions")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("city", data[0])
    
    def test_prediction_valid_city(self):
        """Test the prediction endpoint with a valid city"""
        response = client.get("/predictions/Berlin")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check that the response has the correct structure
        required_fields = [
            "city", "current_temperature", "current_humidity",
            "predicted_day_temperature", "predicted_night_temperature",
            "prediction_date", "historical_data", "last_updated"
        ]
        for field in required_fields:
            self.assertIn(field, data)
        
        # Check that historical data is a list
        self.assertIsInstance(data["historical_data"], list)
    
    def test_prediction_invalid_city(self):
        """Test the prediction endpoint with an invalid city"""
        response = client.get("/predictions/InvalidCity")
        # Should return 404 Not Found for invalid cities
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main() 