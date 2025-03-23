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
├── frontend/             # Frontend application
├── .env                  # Environment variables
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Airflow Dockerfile
├── Dockerfile.api        # FastAPI Dockerfile
├── Dockerfile.frontend   # Frontend Dockerfile
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Features

### Data Collection and Processing
- Collects weather data (temperature and humidity) for 5 German cities using OpenWeatherMap API v3.0
- Stores data in a PostgreSQL database
- Automated daily data collection at 1:00 AM
- Historical data collection for the past 5 days

### Machine Learning
- Trains a linear regression model for each city using:
  - Historical temperature data
  - Day of year (seasonality)
  - Day of week
  - Humidity
- Models are automatically retrained daily with new data
- Predictions are stored in the database

### Backend API (FastAPI)
- RESTful API endpoints for weather data and predictions
- CORS enabled for frontend access
- Timezone-aware responses (all times in Europe/Berlin timezone)
- Endpoints:
  - GET /: List available cities
  - GET /predictions: Get predictions for all cities
  - GET /predictions/{city}: Get prediction for specific city

### Frontend Application
- Modern, responsive design with Bootstrap and Font Awesome
- Features:
  - City selection dropdown
  - Current weather display with real-time updates
  - Next day temperature prediction
  - Historical data view (last 5 days at 12:00 PM)
  - Loading states and error handling
- Layout:
  - Weather icon in header
  - Left panel for city selection
  - Right panel showing:
    - Current weather with timestamp
    - Tomorrow's prediction
    - Historical data in chronological order

## Setup

1. Clone this repository
2. Create a `.env` file with your OpenWeatherMap API key:

```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

3. Start the services using Docker Compose:

```bash
docker-compose up -d
```

4. Access the services:
   - Frontend: http://localhost:3000
   - Airflow: http://localhost:8080 (Login with username: admin, password: admin)
   - FastAPI: http://localhost:8000/docs

## Automated Processes

### Daily Updates (1:00 AM)
1. Collects new weather data
2. Updates historical records
3. Retrains models with latest data
4. Generates new predictions

### Data Management
- Historical data shows the last 5 days
- Automatically removes older entries
- Stores one reading per day at 12:00 PM
- All timestamps are in German local time (Europe/Berlin)

## Cities Covered

The following German cities are included:
- Berlin
- Munich
- Hamburg
- Frankfurt
- Cologne

## Dependencies

Key dependencies include:
- Apache Airflow
- FastAPI
- scikit-learn
- PostgreSQL
- React (for frontend)
- Bootstrap 5
- Font Awesome
- pytz (for timezone handling)

## Notes

- The frontend automatically refreshes data when clicking "Get Weather"
- All times are displayed in German local time (UTC+1/UTC+2)
- Historical data is collected daily at 12:00 PM
- Models are retrained daily with the latest data
- The system uses Docker for containerization and easy deployment