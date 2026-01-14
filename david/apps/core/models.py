from django.db import models
from django.utils.translation import gettext_lazy as _


class Log(models.Model):
    """
    Model representing a Python logger message.

    Stores log entries with metadata including logger name, message,
    source filename, log level, and timestamp.

    Attributes:
        name: Logger name (e.g., "david.apps.core")
        msg: Log message content
        filename: Source filename where the log was generated
        levelname: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        asctime: Timestamp when the log entry was created
    """

    name = models.CharField(max_length=100, help_text="Logger name")
    msg = models.TextField(help_text="Log message content")
    filename = models.CharField(max_length=100, help_text="Source filename")
    levelname = models.CharField(max_length=100, help_text="Log level")
    asctime = models.DateTimeField(help_text="Log timestamp")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("log")
        verbose_name_plural = _("logs")

    def __str__(self) -> str:
        """Return string representation of the log entry."""
        return f"Log at {self.asctime}"
