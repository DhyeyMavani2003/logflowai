from django.db import models


class LogEntry(models.Model):
    """
    LogEntry model representing a log event with various details such as timestamp, level,
    message, service, host, and additional data. This class stores log events produced by 
    various services and allows for the inclusion of extra structured data.

    Parameters
    ----------
    id : int
        A unique identifier for the log entry (primary key).
    timestamp : datetime, optional
        The datetime when the log was recorded.
    level : str, optional
        The severity level of the log event (e.g., INFO, WARN, ERROR).
    message : str, optional
        The log message providing details about the event.
    service : str, optional
        The service or component that produced the log.
    host : str, optional
        The hostname or IP address of the machine where the log originated.
    additional_data : dict, optional
        Any additional structured data stored as JSON.

    Methods
    -------
    __str__()
        Returns a string representation of the log entry in the format:
        [timestamp] level: message.
    """

    timestamp = models.DateTimeField(null=True)
    level = models.CharField(max_length=20, null=True)
    message = models.TextField(null=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    additional_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message}"
