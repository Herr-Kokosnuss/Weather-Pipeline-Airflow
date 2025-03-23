import os
import sys
from datetime import datetime, timedelta
from utils import CITIES, fetch_weather_data, store_weather_data, create_tables_if_not_exist

def collect_historical_data(days=5):
    """Collect historical weather data for the past 'days' days"""
    print(f"Collecting historical weather data for the past {days} days...")
    
    # Create tables if they don't exist
    create_tables_if_not_exist()
    
    # Get current date
    now = datetime.now()
    
    # Collect data for each city
    for city in CITIES:
        print(f"Collecting data for {city}...")
        
        # Collect data for the past 'days' days at 12:00 PM
        for i in range(1, days + 1):
            # Calculate the date (days ago at 12:00 PM)
            target_date = (now - timedelta(days=i)).replace(hour=12, minute=0, second=0, microsecond=0)
            
            # Fetch weather data
            weather_data = fetch_weather_data(city, target_date)
            
            if weather_data:
                # Store in database
                store_weather_data(weather_data)
                print(f"  - Stored data for {city} on {target_date}")
            else:
                print(f"  - Failed to fetch data for {city} on {target_date}")
    
    print("Historical data collection completed!")

if __name__ == "__main__":
    # Get number of days from command line argument, default to 5
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    collect_historical_data(days) 