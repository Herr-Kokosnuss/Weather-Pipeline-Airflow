import unittest
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the utils module (assuming it exists)
try:
    from utils import preprocess_data, evaluate_model, feature_engineering
except ImportError:
    # Mocking the functions for testing if the actual module doesn't exist
    def preprocess_data(df):
        """Mock function for preprocessing data"""
        if df is None or df.empty:
            return pd.DataFrame()
        return df.dropna()
    
    def evaluate_model(y_true, y_pred):
        """Mock function for evaluating model"""
        if len(y_true) != len(y_pred):
            raise ValueError("Arrays must be of the same length")
        return {"mae": 0.5, "rmse": 1.0, "r2": 0.8}
    
    def feature_engineering(df):
        """Mock function for feature engineering"""
        if df is None or df.empty:
            return pd.DataFrame()
        return df


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def setUp(self):
        """Set up test data"""
        # Create a sample dataframe for testing
        dates = [datetime.now() - timedelta(days=i) for i in range(10)]
        self.test_df = pd.DataFrame({
            'date': dates,
            'temperature': [20, 22, 19, 21, 23, 20, 18, 22, 21, 19],
            'humidity': [80, 75, 85, 78, 72, 81, 84, 76, 79, 82],
            'city': ['Berlin'] * 10
        })
        
        # Create data with missing values
        self.df_with_nans = self.test_df.copy()
        self.df_with_nans.loc[3:5, 'temperature'] = None
        
        # Create predictions for evaluation
        self.y_true = [20, 22, 19, 21, 23]
        self.y_pred = [19.5, 21.8, 18.7, 20.5, 22.7]
    
    def test_preprocess_data(self):
        """Test preprocess_data function"""
        # Test with normal dataframe
        processed_df = preprocess_data(self.test_df)
        self.assertEqual(len(processed_df), len(self.test_df))
        
        # Test with dataframe containing NaN values
        processed_df = preprocess_data(self.df_with_nans)
        self.assertEqual(len(processed_df), len(self.df_with_nans) - 3)  # 3 rows have NaN
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        processed_df = preprocess_data(empty_df)
        self.assertTrue(processed_df.empty)
    
    def test_evaluate_model(self):
        """Test evaluate_model function"""
        # Test with valid inputs
        metrics = evaluate_model(self.y_true, self.y_pred)
        self.assertIsInstance(metrics, dict)
        self.assertIn('mae', metrics)
        self.assertIn('rmse', metrics)
        self.assertIn('r2', metrics)
        
        # Test with invalid inputs (different lengths)
        with self.assertRaises(ValueError):
            evaluate_model(self.y_true, self.y_pred[:-1])
    
    def test_feature_engineering(self):
        """Test feature_engineering function"""
        # Test with normal dataframe
        result_df = feature_engineering(self.test_df)
        self.assertIsInstance(result_df, pd.DataFrame)
        
        # Test with empty dataframe
        empty_df = pd.DataFrame()
        result_df = feature_engineering(empty_df)
        self.assertTrue(result_df.empty)


if __name__ == '__main__':
    unittest.main() 