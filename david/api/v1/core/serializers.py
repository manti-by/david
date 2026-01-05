from datetime import datetime
from logging import getLevelNamesMapping

from django.utils import timezone
from rest_framework import serializers


class LogSerializer(serializers.Serializer):
    """
    Serializer for log entry creation.

    Validates and serializes log data from Python logging module format.
    All fields are required.

    Fields:
        name: Logger name (max 100 chars, e.g., "david.apps.core")
        msg: Log message content
        filename: Source filename (max 100 chars)
        levelname: Log level - must be valid Python logging level
        asctime: Timestamp - must not be in the future
    """

    name = serializers.CharField(max_length=100, help_text="Logger name (e.g., 'david.apps.core')")
    msg = serializers.CharField(help_text="Log message content")
    filename = serializers.CharField(max_length=100, help_text="Source filename")
    levelname = serializers.ChoiceField(
        choices=list(getLevelNamesMapping().keys()),
        help_text="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    asctime = serializers.DateTimeField(help_text="Log timestamp (must not be in the future)")

    def validate_asctime(self, value: datetime) -> datetime:
        """
        Validate that the timestamp is not in the future.

        Args:
            value: DateTime value to validate

        Returns:
            Validated datetime value

        Raises:
            ValidationError: If timestamp is in the future
        """
        if value > timezone.now():
            raise serializers.ValidationError("Log timestamp cannot be in the future.")
        return value


class HealthcheckCheckSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["healthy", "unhealthy"])
    message = serializers.CharField(allow_blank=True, required=False, default="")


class HealthcheckChecksSerializer(serializers.Serializer):
    database = HealthcheckCheckSerializer()
    cache = HealthcheckCheckSerializer()
    celery = HealthcheckCheckSerializer()


class HealthcheckSerializer(serializers.Serializer):
    """
    Serializer for healthcheck responses.

    Example structure:
    {
        "status": "healthy" | "degraded",
        "checks": {
            "database": {"status": "healthy" | "unhealthy", "message": "..."},
            "cache": {"status": "healthy" | "unhealthy", "message": "..."},
            "celery": {"status": "healthy" | "unhealthy", "message": "..."}
        }
    }
    """

    status = serializers.ChoiceField(choices=["healthy", "degraded"])
    checks = HealthcheckChecksSerializer()
