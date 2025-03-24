FROM apache/airflow:2.7.1

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir -p /opt/airflow/scripts /opt/airflow/models /opt/airflow/dags

COPY dags/ /opt/airflow/dags/
COPY scripts/ /opt/airflow/scripts/
COPY models/ /opt/airflow/models/

WORKDIR /opt/airflow 