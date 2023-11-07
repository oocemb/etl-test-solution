LOG_FORMAT = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
PATH_LOGS_FILE = "./etl_app.log"
LOG_DEFAULT_HANDLERS = ["console", "file"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": PATH_LOGS_FILE,
            "formatter": "verbose",
            "encoding": "utf-8",
            'when': 'D',  # День
            "interval": 30,  # 30 дней 1 файл лога
            "backupCount": 6  # Если не 0 сохраняет не более <> файлов (6 раз по 30 дней храним)
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
    },
    "root": {
        "level": "DEBUG",
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
