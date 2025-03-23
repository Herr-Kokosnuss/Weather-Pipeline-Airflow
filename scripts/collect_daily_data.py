import os
from datetime import datetime, timedelta
from utils import CITIES, fetch_weather_data, store_weather_data, create_tables_if_not_exist

def collect_daily_data():
    """Collect weather data for yesterday at 12:00 PM"""
    print("Collecting daily weather data...")
    
    # Create tables if they don't exist
    create_tables_if_not_exist()
    
    # Calculate yesterday at 12:00 PM
    yesterday_noon = (datetime.now() - timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
    
    # Collect data for each city
    for city in CITIES:
        print(f"Collecting data for {city} at {yesterday_noon}...")
        
        # Fetch weather data
        weather_data = fetch_weather_data(city, yesterday_noon)
        
        if weather_data:
            # Store in database
            store_weather_data(weather_data)
            print(f"  - Stored data for {city}")
        else:
            print(f"  - Failed to fetch data for {city}")
    
    print("Daily data collection completed!")

if __name__ == "__main__":
    collect_daily_data() 