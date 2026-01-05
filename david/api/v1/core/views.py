from celery.exceptions import CeleryError
from psycopg2 import DatabaseError
from redis.exceptions import RedisError

from django.core.cache import cache
from django.db import connection
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from david.api.v1.core.serializers import HealthcheckSerializer, LogSerializer
from david.apps.core.celery import app as celery_app
from david.apps.core.models import Log


class HealthCheckView(RetrieveAPIView):
    """
    Health check endpoint for monitoring system status.

    Verifies connectivity and health of:
    - Database (PostgreSQL)
    - Cache (Redis)
    - Celery broker (RabbitMQ)

    Returns:
        - 200 OK: All services are healthy
        - 503 Services Unavailable: One or more services are unhealthy

    Response format:
    {
        "status": "healthy" | "degraded",
        "checks": {
            "database": {"status": "healthy" | "unhealthy", "message": "..."},
            "cache": {"status": "healthy" | "unhealthy", "message": "..."},
            "celery": {"status": "healthy" | "unhealthy", "message": "..."}
        }
    }
    """

    permission_classes = (AllowAny,)
    serializer_class = HealthcheckSerializer

    def get(self, request: Request, *args: list, **kwargs: dict) -> HttpResponse:
        """
        Perform health checks on all system components.

        Returns a comprehensive health status report.
        """
        health_status = {
            "status": "healthy",
            "checks": {
                "database": self._check_database(),
                "cache": self._check_cache(),
                "celery": self._check_celery(),
            },
        }

        # Determine overall status
        all_healthy = all(check["status"] == "healthy" for check in health_status["checks"].values())
        health_status["status"] = "healthy" if all_healthy else "degraded"

        # Return appropriate HTTP status code
        http_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(health_status, status=http_status)

    @staticmethod
    def _check_database() -> dict:
        """Check database connectivity."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return {"status": "healthy", "message": "Database connection successful"}
        except DatabaseError as e:
            return {"status": "unhealthy", "message": f"Database connection failed: {e!s}"}

    @staticmethod
    def _check_cache() -> dict:
        """Check cache (Redis) connectivity."""
        try:
            # Try to set and get a test value
            test_key = "health_check_test"
            test_value = "test"
            cache.set(test_key, test_value, timeout=1)
            retrieved = cache.get(test_key)
            if retrieved == test_value:
                cache.delete(test_key)
                return {"status": "healthy", "message": "Cache connection successful"}
            return {"status": "unhealthy", "message": "Cache read/write test failed"}
        except RedisError as e:
            return {"status": "unhealthy", "message": f"Cache connection failed: {e!s}"}

    @staticmethod
    def _check_celery() -> dict:
        """Check RabbitMQ broker connectivity."""
        try:
            with celery_app.connection() as conn:
                conn.connect()
            return {
                "status": "healthy",
                "message": "Celery broker connection successful",
            }
        except CeleryError as e:
            return {"status": "unhealthy", "message": f"Celery broker check failed: {e!s}"}


class LogsView(CreateAPIView):
    """
    API endpoint for creating log entries.

    Accepts log data including
    - name: Logger name (e.g., "david.apps.core")
    - msg: Log message content
    - filename: Source filename
    - levelname: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - asctime: Timestamp (must not be in the future)

    Returns:
        - 201 Created: Log entry successfully created
        - 400 Bad Request: Validation error
    """

    serializer_class = LogSerializer

    def perform_create(self, serializer: LogSerializer) -> Log:
        """
        Create a new log entry from validated serializer data.

        Args:
            serializer: Validated LogSerializer instance

        Returns:
            Created Log instance
        """
        return Log.objects.create(**serializer.validated_data)
