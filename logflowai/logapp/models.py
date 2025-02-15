from django.db import models

class LogEntry(models.Model):
    line_id = models.IntegerField(unique=True)
    date = models.CharField(max_length=10)  # Format: YYYYMMDD
    time = models.CharField(max_length=10)  # Format: HHMMSS
    pid = models.IntegerField()
    level = models.CharField(max_length=10, choices=[
        ('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('CRITICAL', 'CRITICAL')
    ])
    component = models.CharField(max_length=100)
    content = models.TextField()
    event_id = models.CharField(max_length=10)
    event_template = models.TextField()

    @classmethod
    def import_from_csv(cls, csv_path):
        import pandas as pd
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            cls.objects.update_or_create(
                line_id=row['LineId'],
                defaults={
                    'date': row['Date'],
                    'time': row['Time'],
                    'pid': row['Pid'],
                    'level': row['Level'],
                    'component': row['Component'],
                    'content': row['Content'],
                    'event_id': row['EventId'],
                    'event_template': row['EventTemplate']
                }
            )

    def __str__(self):
        return f"{self.date} {self.time} - {self.level} - {self.component}"