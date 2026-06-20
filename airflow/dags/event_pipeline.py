from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="event_pipeline",
    start_date=datetime(2025,1,1),
    schedule=None,
    catchup=False,
    tags=["genpact"]
) as dag: