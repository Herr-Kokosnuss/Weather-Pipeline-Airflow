import unittest
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def clean_data(df):
    """Mock function for data cleaning"""
    if df is None or df.empty:
        return pd.DataFrame()
    return df.dropna()

def calculate_metrics(actual, predicted):
    """Mock function for metric calculation"""
    if len(actual) != len(predicted):
        raise ValueError("Arrays must be of same length")
    return {
        "mae": 0.5,
        "rmse": 1.0
    }

def format_date(date):
    """Mock function for date formatting"""
    return date.strftime("%Y-%m-%d")

class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = pd.DataFrame({
            'date': [datetime.now()] * 5,
            'temperature': [20, 22, 19, 21, 23],
            'humidity': [80, 75, 85, 78, 72],
            'city': ['Berlin'] * 5
        })
        
        self.data_with_nulls = self.test_data.copy()
        self.data_with_nulls.loc[0, 'temperature'] = None
    
    def test_clean_data(self):
        """Test data cleaning function"""
        cleaned = clean_data(self.test_data)
        self.assertEqual(len(cleaned), len(self.test_data))
        self.assertTrue(cleaned['temperature'].notna().all())
        
        cleaned = clean_data(self.data_with_nulls)
        self.assertEqual(len(cleaned), len(self.data_with_nulls) - 1)
    
    def test_calculate_metrics(self):
        """Test metric calculation"""
        actual = [20, 22, 19, 21, 23]
        predicted = [19.5, 21.8, 18.7, 20.5, 22.7]
        
        metrics = calculate_metrics(actual, predicted)
        
        self.assertIsInstance(metrics['mae'], float)
        self.assertIsInstance(metrics['rmse'], float)
        
        self.assertGreaterEqual(metrics['mae'], 0)
        self.assertGreaterEqual(metrics['rmse'], 0)
    
    def test_format_date(self):
        """Test date formatting"""
        test_date = datetime.now()
        formatted = format_date(test_date)
        
        self.assertIsInstance(formatted, str)
        self.assertEqual(len(formatted.split('-')), 3)

if __name__ == '__main__':
    unittest.main() 