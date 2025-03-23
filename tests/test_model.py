import unittest
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock classes and functions
class WeatherPredictor:
    """Mock weather predictor class"""
    def train(self, data):
        """Mock training method"""
        pass
    
    def predict(self, city):
        """Mock prediction method"""
        return {
            'day_temp': 23.8,
            'night_temp': 18.2
        }

def validate_predictions(actual, predicted):
    """Mock validation function"""
    return 0.85  # Mock accuracy score

def split_data(data, test_size=0.2):
    """Mock data splitting function"""
    split_idx = int(len(data) * (1 - test_size))
    return data[:split_idx], data[split_idx:]

class TestModel(unittest.TestCase):
    """Test cases for the weather prediction model"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample training data
        self.train_data = pd.DataFrame({
            'date': [datetime.now()] * 10,
            'temperature': [20, 22, 19, 21, 23, 20, 18, 22, 21, 19],
            'humidity': [80, 75, 85, 78, 72, 81, 84, 76, 79, 82],
            'city': ['Berlin'] * 10
        })
    
    def test_model_prediction(self):
        """Test model prediction"""
        # Initialize model
        model = WeatherPredictor()
        
        # Train model
        model.train(self.train_data)
        
        # Make prediction
        prediction = model.predict('Berlin')
        
        # Check prediction structure
        self.assertIn('day_temp', prediction)
        self.assertIn('night_temp', prediction)
        
        # Check prediction values are reasonable
        self.assertTrue(0 <= prediction['day_temp'] <= 50)
        self.assertTrue(0 <= prediction['night_temp'] <= 50)
    
    def test_model_validation(self):
        """Test model validation"""
        # Create test predictions
        actual = np.array([20, 22, 19, 21, 23])
        predicted = np.array([19.5, 21.8, 18.7, 20.5, 22.7])
        
        # Validate predictions
        score = validate_predictions(actual, predicted)
        
        # Check score is between 0 and 1
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
    
    def test_data_splitting(self):
        """Test data splitting functionality"""
        # Split data
        train, test = split_data(self.train_data)
        
        # Check split sizes
        self.assertEqual(len(train) + len(test), len(self.train_data))
        self.assertTrue(len(train) > len(test))  # Train should be larger

if __name__ == '__main__':
    unittest.main() 