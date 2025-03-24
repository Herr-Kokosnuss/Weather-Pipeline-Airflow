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
    
    df = get_training_data(city)
    
    if df is None or len(df) < 3:  # Need at least 3 data points for meaningful training
        print(f"  - Not enough data for {city}, skipping...")
        return False
    
    df['day_of_year'] = df['timestamp'].dt.dayofyear
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    df = df.sort_values('timestamp')
    
    X = df[['day_of_year', 'day_of_week', 'humidity']].values
    y = df['temperature'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    city_dir = f"/opt/airflow/models/{city}"
    os.makedirs(city_dir, exist_ok=True)
    
    model_path = f"{city_dir}/temperature_model.pkl"
    joblib.dump(model, model_path)
    print(f"  - Model saved to {model_path}")
    
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_features = np.array([
        [tomorrow.timetuple().tm_yday, tomorrow.weekday(), df['humidity'].mean()]
    ])
    
    predicted_temp = model.predict(tomorrow_features)[0]
    
    store_prediction(city, tomorrow.date(), predicted_temp)
    
    print(f"  - Model trained for {city}")
    print(f"  - Predicted temperature for {tomorrow.date()}: {predicted_temp:.2f}°C")
    
    return True

def train_all_models():
    """Train models for all cities"""
    print("Training models for all cities...")
    
    create_tables_if_not_exist()
    
    success_count = 0
    
    for city in CITIES:
        if train_model_for_city(city):
            success_count += 1
    
    print(f"Model training completed! Successfully trained {success_count}/{len(CITIES)} models.")

if __name__ == "__main__":
    train_all_models() 