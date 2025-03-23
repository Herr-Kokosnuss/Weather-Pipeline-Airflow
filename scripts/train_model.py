import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
from sklearn.linear_model import LinearRegression
from utils import CITIES, get_training_data, store_prediction, create_tables_if_not_exist

def train_model_for_city(city):
    """Train a model for a specific city and make prediction for the next day"""
    print(f"Training model for {city}...")
    
    # Get training data
    df = get_training_data(city)
    
    if df is None or len(df) < 3:  # Need at least 3 data points for meaningful training
        print(f"  - Not enough data for {city}, skipping...")
        return False
    
    # Prepare features and target
    df['day_of_year'] = df['timestamp'].dt.dayofyear
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Sort by timestamp (oldest first)
    df = df.sort_values('timestamp')
    
    # Features: day of year, day of week, humidity
    X = df[['day_of_year', 'day_of_week', 'humidity']].values
    # Target: temperature
    y = df['temperature'].values
    
    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Create the city directory if it doesn't exist
    city_dir = f"/opt/airflow/models/{city}"
    os.makedirs(city_dir, exist_ok=True)
    
    # Save the model
    model_path = f"{city_dir}/temperature_model.pkl"
    joblib.dump(model, model_path)
    print(f"  - Model saved to {model_path}")
    
    # Make prediction for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_features = np.array([
        [tomorrow.timetuple().tm_yday, tomorrow.weekday(), df['humidity'].mean()]
    ])
    
    # Use the model to predict temperature for all cities
    predicted_temp = model.predict(tomorrow_features)[0]
    
    # Store prediction
    store_prediction(city, tomorrow.date(), predicted_temp)
    
    print(f"  - Model trained for {city}")
    print(f"  - Predicted temperature for {tomorrow.date()}: {predicted_temp:.2f}°C")
    
    return True

def train_all_models():
    """Train models for all cities"""
    print("Training models for all cities...")
    
    # Create tables if they don't exist
    create_tables_if_not_exist()
    
    success_count = 0
    
    for city in CITIES:
        if train_model_for_city(city):
            success_count += 1
    
    print(f"Model training completed! Successfully trained {success_count}/{len(CITIES)} models.")

if __name__ == "__main__":
    train_all_models() 