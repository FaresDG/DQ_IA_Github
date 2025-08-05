from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def hello_world():
    print("Hello from Airflow")

with DAG(
    dag_id="example_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
):
    PythonOperator(task_id="hello", python_callable=hello_world)