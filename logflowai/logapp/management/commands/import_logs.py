import csv
import os
import json
from datetime import datetime
import pytz
from django.core.management.base import BaseCommand
from logapp.models import LogEntry

class Command(BaseCommand):
    help = "Imports log entries from HDFS_2k.log_structured.csv file"

    def handle(self, *args, **options):
        # Path relative to your project root
        file_path = os.path.join('logapp', 'data', 'HDFS_2k.log_structured.csv')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        count = 0
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # CSV columns: LineId,Date,Time,Pid,Level,Component,Content,EventId,EventTemplate
                date_str = row.get('Date')    # e.g. "081109" (MMDDYY)
                time_str = row.get('Time')    # e.g. "203615" (HHMMSS)
                timestamp = None
                if date_str and time_str:
                    try:
                        # Combine Date and Time into a datetime object.
                        dt = datetime.strptime(date_str + time_str, "%m%d%y%H%M%S")
                        # Assume timestamp is in UTC (adjust as needed)
                        timestamp = dt.replace(tzinfo=pytz.UTC)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Error parsing timestamp: {date_str} {time_str}: {e}"))
                        timestamp = None

                level = row.get('Level')      # e.g. "INFO"
                message = row.get('Content')    # the log message
                service = row.get('Component')  # use Component as service name
                host = ""                     # no host provided in CSV

                # Save extra columns as additional data
                additional_data = {
                    'LineId': row.get('LineId'),
                    'Pid': row.get('Pid'),
                    'EventId': row.get('EventId'),
                    'EventTemplate': row.get('EventTemplate')
                }

                # Create and save the log entry
                log_entry = LogEntry(
                    timestamp=timestamp,
                    level=level,
                    message=message,
                    service=service,
                    host=host,
                    additional_data=additional_data,
                )
                log_entry.save()
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} log entries."))
