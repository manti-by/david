import os

from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ("david.local",)

SECRET_KEY = os.getenv("SECRET_KEY")

# CSRF settings

if csrf_trusted_origins := os.getenv("CSRF_TRUSTED_ORIGINS", ""):
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted_origins.split(",") if origin.strip()]

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = "Strict"

CSRF_USE_SESSIONS = False

# Security Headers

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365  # 1 year

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

# Database overrides

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_NAME", "david"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASS"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}

# RabbitMQ overrides

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbitmq_user = os.getenv("RABBITMQ_USER")
rabbitmq_pass = os.getenv("RABBITMQ_PASS")

CELERY_BROKER_URL = f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:5672/david"

# Production logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "/var/log/app/django.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {"handlers": ["console", "file"], "level": "WARNING"},
    },
}
