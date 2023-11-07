import logging
from datetime import timedelta
from logging import config

from pydantic import BaseSettings

from logger_conf import LOGGING

config.dictConfig(LOGGING)
logger = logging.getLogger()


default_args = {
    "owner": "GruzdevAV",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    # "email": ["<Example>@gmail.com"],
    # "email_on_failure": True,
    # "email_on_retry": True
}


class ETLSettings(BaseSettings):
    PATH_TO_FILES_DOCKER: str = "/opt/airflow/files_folder/"


settings = ETLSettings()
