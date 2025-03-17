import os
import requests
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

CITIES = [
    "Berlin",
    "Munich",
    "Hamburg",
    "Frankfurt",
    "Cologne"
]

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "airflow"),
        user=os.getenv("POSTGRES_USER", "airflow"),
        password=os.getenv("POSTGRES_PASSWORD", "airflow"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    return conn

def create_tables_if_not_exist():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            temperature FLOAT NOT NULL,
            humidity FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_predictions (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            prediction_date DATE NOT NULL,
            predicted_temperature FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

def fetch_weather_data(city, timestamp=None):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if timestamp:
        unix_time = int(timestamp.timestamp())
        url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={get_city_coordinates(city)[0]}&lon={get_city_coordinates(city)[1]}&dt={unix_time}&appid={api_key}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={get_city_coordinates(city)[0]}&lon={get_city_coordinates(city)[1]}&appid={api_key}&units=metric&exclude=minutely,hourly,daily,alerts"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if timestamp:
            weather_data = {
                'city': city,
                'timestamp': timestamp,
                'temperature': data['data'][0]['temp'],
                'humidity': data['data'][0]['humidity']
            }
        else:
            weather_data = {
                'city': city,
                'timestamp': datetime.fromtimestamp(data['current']['dt']),
                'temperature': data['current']['temp'],
                'humidity': data['current']['humidity']
            }
        
        return weather_data
    else:
        print(f"Error fetching data for {city}: {response.status_code} - {response.text}")
        return None

def get_city_coordinates(city):
    coordinates = {
        "Berlin": (52.5200, 13.4050),
        "Munich": (48.1351, 11.5820),
        "Hamburg": (53.5511, 9.9937),
        "Frankfurt": (50.1109, 8.6821),
        "Cologne": (50.9375, 6.9603)
    }
    
    return coordinates.get(city, (0, 0))

def store_weather_data(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO weather_data (city, timestamp, temperature, humidity)
        VALUES (%s, %s, %s, %s)
        """,
        (data['city'], data['timestamp'], data['temperature'], data['humidity'])
    )
    
    conn.commit()
    cursor.close()
    conn.close()

def store_prediction(city, prediction_date, predicted_temperature):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO weather_predictions (city, prediction_date, predicted_temperature)
        VALUES (%s, %s, %s)
        """,
        (city, prediction_date, predicted_temperature)
    )
    
    conn.commit()
    cursor.close()
    conn.close()

def get_training_data(city, days=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT timestamp, temperature, humidity
        FROM weather_data
        WHERE city = %s
        ORDER BY timestamp DESC
        LIMIT %s
        """,
        (city, days)
    )
    
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if data:
        df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'humidity'])
        return df
    else:
        return None

def get_latest_prediction(city):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT prediction_date, predicted_temperature, created_at
        FROM weather_predictions
        WHERE city = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (city,)
    )
    
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if data:
        return {
            'city': city,
            'prediction_date': data[0],
            'predicted_temperature': data[1],
            'created_at': data[2]
        }
    else:
        return None