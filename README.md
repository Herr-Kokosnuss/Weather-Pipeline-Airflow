# Weather Prediction Pipeline

This project implements an ML-Ops pipeline using Airflow to collect weather data, train a simple ML model, and predict the temperature for the next day.

## Project Structure

```
.
├── api/                  # FastAPI application
├── dags/                 # Airflow DAGs
├── data/                 # Data storage
├── models/               # Trained models
├── scripts/              # Python scripts
├── .env                  # Environment variables
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Airflow Dockerfile
├── Dockerfile.api        # FastAPI Dockerfile
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Features

- Collects weather data (temperature and humidity) for 5 German cities using OpenWeatherMap API v3.0
- Stores data in a PostgreSQL database
- Trains a simple linear regression model to predict the next day's temperature
- Provides a FastAPI endpoint to access predictions
- Scheduled to run daily at 1:00 AM to collect data from the previous day at 12:00 PM

## Setup

1. Clone this repository
2. Create a `.env` file with your OpenWeatherMap API key (requires a subscription to the One Call API v3.0):

```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

3. Start the services using Docker Compose:

```bash
docker-compose up -d
```

> **Note:** 
> If you want to modify the Airflow admin user credentials (username, password, email, etc.), edit the command in the `airflow-init` service in the `docker-compose.yml` file before running `docker-compose up -d`.


4. Access the Airflow web interface at http://localhost:8080 (Login with username: admin, password: admin)

5. Trigger the initial data collection DAG:
   - Go to the Airflow web interface
   - Find the `weather_initial_data_collection` DAG
   - Click on the "Trigger DAG" button

6. The daily data collection will run automatically at 1:00 AM every day

## API Endpoints

The FastAPI application provides the following endpoints:

- `GET /`: Welcome message and available endpoints
- `GET /predictions`: Get predictions for all cities
- `GET /predictions/{city}`: Get prediction for a specific city

Access the API documentation at http://localhost:8000/docs

## Cities

The following German cities are included in the pipeline:

- Berlin
- Munich
- Hamburg
- Frankfurt
- Cologne

## ML Model

The ML model is a simple linear regression that uses the following features:
- Day of year
- Day of week
- Humidity

The model is trained to predict the temperature for the next day. 