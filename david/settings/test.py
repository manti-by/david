from .base import *  # noqa

DEBUG = False

# Use in-memory Redis for testing
CELERY_BROKER_URL = "memory://"
CELERY_TASK_ALWAYS_EAGER = True

ALLOWED_HOSTS = ("*",)

MEDIA_ROOT = "/tmp/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "ERROR"},
    },
}
