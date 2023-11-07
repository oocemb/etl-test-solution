from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from settings import default_args
from xlsx_handler import insert_overdue_raw_data


@dag(dag_id="Handle_overdue_dag_v1",
     default_args=default_args,
     start_date=datetime(2023, 8, 9),
     schedule=None,
     tags=["postgres", "init"])
def handle_overdue_dag():

    task1 = BashOperator(
        task_id="scan_files_folder",
        bash_command="echo scan files_folder"
    )
    task2 = PythonOperator(
        task_id="insert_overdue_raw_data",
        python_callable=insert_overdue_raw_data
    )
    task1 >> task2  # noqa


new_dag = handle_overdue_dag()
