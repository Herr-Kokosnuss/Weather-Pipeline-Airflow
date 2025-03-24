import os
import sys
from datetime import datetime, timedelta
from utils import CITIES, fetch_weather_data, store_weather_data, create_tables_if_not_exist

def collect_historical_data(days=5):
    """Collect historical weather data for the past 'days' days"""
    print(f"Collecting historical weather data for the past {days} days...")
    
    create_tables_if_not_exist()
    
    now = datetime.now()
    
    for city in CITIES:
        print(f"Collecting data for {city}...")
        
        for i in range(1, days + 1):
            target_date = (now - timedelta(days=i)).replace(hour=12, minute=0, second=0, microsecond=0)
            
            weather_data = fetch_weather_data(city, target_date)
            
            if weather_data:
                store_weather_data(weather_data)
                print(f"  - Stored data for {city} on {target_date}")
            else:
                print(f"  - Failed to fetch data for {city} on {target_date}")
    
    print("Historical data collection completed!")

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    collect_historical_data(days) 