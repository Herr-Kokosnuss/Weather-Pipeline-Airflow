import unittest
import sys
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MOCK_CITIES = ["Berlin", "Munich", "Hamburg"]

app = FastAPI(title="Weather ML API Mock")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/cities")
def get_cities():
    return MOCK_CITIES

@app.get("/predictions/{city}")
def get_prediction(city: str):
    if city not in MOCK_CITIES:
        raise HTTPException(status_code=404, detail=f"City not found. Available cities: {', '.join(MOCK_CITIES)}")
    
    return {
        "city": city,
        "temperature": 21.5,
        "humidity": 75,
        "prediction": {
            "day_temp": 23.8,
            "night_temp": 18.2
        }
    }

client = TestClient(app)

class TestAPI(unittest.TestCase):
    """Test cases for the API endpoints"""
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")
    
    def test_get_cities(self):
        """Test getting list of available cities"""
        response = client.get("/cities")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
    
    def test_get_prediction(self):
        """Test getting prediction for a valid city"""
        response = client.get("/predictions/Berlin")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check required fields
        required_fields = [
            "city",
            "temperature",
            "humidity",
            "prediction"
        ]
        for field in required_fields:
            self.assertIn(field, data)
        
        # Check prediction structure
        self.assertIn("day_temp", data["prediction"])
        self.assertIn("night_temp", data["prediction"])
    
    def test_invalid_city(self):
        """Test response for invalid city"""
        response = client.get("/predictions/InvalidCity")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 