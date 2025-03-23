from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os
import sys

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

# Import functions from scripts
from collect_historical_data import collect_historical_data
from collect_daily_data import collect_daily_data
from train_model import train_all_models

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAGs
# 1. Initial data collection and model training DAG (run once)
initial_dag = DAG(
    'weather_initial_data_collection',
    default_args=default_args,
    description='Initial weather data collection and model training',
    schedule_interval=None,  # Run manually
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['weather', 'initial'],
)

# 2. Daily data collection and model training DAG
daily_dag = DAG(
    'weather_daily_prediction',
    default_args=default_args,
    description='Daily weather data collection and model training',
    schedule_interval='0 1 * * *',  # Run at 1:00 AM every day
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['weather', 'daily'],
)

# Define tasks for initial DAG
initial_collect_task = PythonOperator(
    task_id='collect_historical_data',
    python_callable=collect_historical_data,
    op_kwargs={'days': 5},
    dag=initial_dag,
)

initial_train_task = PythonOperator(
    task_id='train_initial_models',
    python_callable=train_all_models,
    dag=initial_dag,
)

# Define tasks for daily DAG
daily_collect_task = PythonOperator(
    task_id='collect_daily_data',
    python_callable=collect_daily_data,
    dag=daily_dag,
)

daily_train_task = PythonOperator(
    task_id='train_daily_models',
    python_callable=train_all_models,
    dag=daily_dag,
)

# Define task dependencies
initial_collect_task >> initial_train_task
daily_collect_task >> daily_train_task 