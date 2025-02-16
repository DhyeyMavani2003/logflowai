from django.db import models


class LogEntry(models.Model):
    """
    LogEntry model representing a log event.

    Fields:
      timestamp: The datetime when the log was recorded.
      level: The severity level (e.g., INFO, WARN, ERROR).
      message: The log message.
      service: The service or component that produced the log.
      host: The hostname or IP of the machine where the log originated.
      additional_data: Any additional structured data stored in JSON.
    """

    timestamp = models.DateTimeField(null=True)
    level = models.CharField(max_length=20, null=True)
    message = models.TextField(null=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    additional_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message}"
