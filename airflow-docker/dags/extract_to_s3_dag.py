from airflow import DAG
from airflow.operators.python import PythonOperator
from extract_to_s3 import get_weather_data
from datetime import datetime

default_args = {
    'owner': 'rofiat',
    'retries': 1
}

dag = DAG(
    dag_id = "daily_lagos_weather_to_s3",
    description = "This is my dag for daily weather extraction to s3",
    start_date = datetime(2025,6,11),
    schedule_interval = "0 10 * * *", # runs daily at 10am 
    catchup= False,
    default_args = default_args
    )

extract_to_s3 = PythonOperator(
    task_id = "extract_to_s3",
    dag = dag,
    python_callable = get_weather_data
    )

extract_to_s3