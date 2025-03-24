# Weather Prediction Pipeline

A weather prediction system that combines data collection, machine learning, and web services to provide temperature forecasts for German cities. The project demonstrates containerization, automated workflows, and modern web development practices.

## Project Structure

```
.
├── api/                  # FastAPI backend service
├── dags/                # Airflow DAG definitions
├── data/                # Data storage
├── models/              # ML model storage
├── scripts/             # Utility scripts
├── frontend/            # React frontend
├── nginx/               # Nginx configuration
└── tests/              # Test suite
```

## Core Components

### Data Pipeline
- Weather data collection using OpenWeatherMap API for 5 German cities
- Airflow-managed daily data collection at 1:00 AM
- PostgreSQL database for data storage
- 5-day historical data retention

### Machine Learning
- Daily temperature prediction using scikit-learn
- Features include:
  - Historical temperature data
  - Day of year (seasonality)
  - Day of week
  - Humidity
- Automated daily model retraining

### Backend Service
- FastAPI-based REST API
- OpenAPI/Swagger documentation
- Endpoints for:
  - City listing
  - Weather predictions
  - Historical data
- Timezone handling (Europe/Berlin)

### Frontend
- React application with Bootstrap
- Features:
  - City selection
  - Current weather display
  - Next day prediction view
  - Historical data visualization
  - AI chat interface using OpenAI

## Development

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Node.js 14+
- OpenWeatherMap API key
- OpenAI API key

### Local Setup

1. Clone the repository
2. Create environment file:
```bash
cp .env.example .env
# Add your API keys:
# - OPENWEATHERMAP_API_KEY
# - OPENAI_API_KEY
```

3. Start services:
```bash
docker-compose up -d
```

4. Access local services:
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs
- Airflow: http://localhost:8080 (login: admin/admin)

## Testing

The project includes:
- Unit tests with pytest
- API integration tests with httpx
- Automated testing in CI pipeline

## Continuous Integration

GitHub Actions workflow includes:
- Code linting and formatting
- Unit and integration tests
- Docker image builds
- Security scanning

## Cities Covered

- Berlin
- Munich
- Hamburg
- Frankfurt
- Cologne

## Dependencies

Key technologies:
- Apache Airflow
- FastAPI
- scikit-learn
- PostgreSQL
- React
- OpenAI
- Docker
- Nginx
