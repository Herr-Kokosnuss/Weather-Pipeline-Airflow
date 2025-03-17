FROM apache/airflow:2.7.1

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements file
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Create directories
RUN mkdir -p /opt/airflow/scripts /opt/airflow/models /opt/airflow/data

# Set working directory
WORKDIR /opt/airflow 