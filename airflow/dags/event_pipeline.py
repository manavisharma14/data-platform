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
    
    load_events = BashOperator(
        task_id="load_events",
        bash_command="python /project/ingestion/load_events.py"
    )

    validate_events = BashOperator(

        task_id="validate_events",

        bash_command="python /project/validation/validate_events.py"

    )

    retry_failed_events = BashOperator(

        task_id="retry_failed_events",

        bash_command="python /project/validation/retry_failed_events.py"

    )

    build_warehouse = BashOperator(

        task_id="build_warehouse",

        bash_command="python /project/warehouse/build_warehouse.py"

    )

    load_events >> validate_events >> retry_failed_events >> build_warehouse