from django.test import TestCase
from datetime import datetime
import pytz
from .models import LogEntry


class LogEntryTestCase(TestCase):
    def setUp(self):
        LogEntry.objects.create(
            timestamp=datetime.now(pytz.UTC),
            level="INFO",
            message="This is a test log entry.",
            service="TestService",
            host="127.0.0.1",
        )

    def test_log_entry_creation(self):
        log = LogEntry.objects.get(service="TestService")
        self.assertEqual(log.level, "INFO")
        self.assertIn("test log", log.message.lower())
