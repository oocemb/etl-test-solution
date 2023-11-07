import logging
from logging import config

from logger_conf import LOGGING

config.dictConfig(LOGGING)
logger = logging.getLogger()

PG_DSL = {
    "dbname": "airflow",
    "user": "airflow",
    "password": "airflow",
    "host": "postgres",
    "port": 5432,
    "options": "-c search_path=public",
}
