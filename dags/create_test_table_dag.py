from datetime import datetime

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator

from settings import default_args


@dag(dag_id="Postgres_initial_dag_v1",
     default_args=default_args,
     start_date=datetime(2023, 8, 9),
     schedule=None,
     tags=["postgres", "init"])
def postgres_operator_dag():
    task1 = PostgresOperator(
        task_id="create_overdue_table",
        postgres_conn_id="pg_localhost",
        sql="""
            CREATE TABLE IF NOT EXISTS public.overdue (
            id serial PRIMARY KEY,
            subject TEXT,
            mo TEXT,
            inn TEXT,
            status TEXT,
            type_out TEXT,
            gtin TEXT,
            series TEXT,
            count_doses_in_pkg integer,
            count_packages integer,
            count_doses_sum integer,
            expiration_date TEXT,
            overdue_day integer
        )"""
    )
    task2 = PostgresOperator(
        task_id="truncate_table_if_exist",
        postgres_conn_id="pg_localhost",
        sql="""
            truncate table overdue;
        """
    )
    task1 >> task2  # noqa


new_dag = postgres_operator_dag()
