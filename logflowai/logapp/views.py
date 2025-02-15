from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import pandas as pd
from .models import LogEntry
from .serializers import LogEntrySerializer

class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all().order_by('-date', '-time')
    serializer_class = LogEntrySerializer

@api_view(['POST'])
def import_logs(request):
    """API to import logs from CSV."""
    file_path = "./data/HDFS_2k.log_structured.csv"
    LogEntry.import_from_csv(file_path)
    return JsonResponse({"message": "Logs imported successfully."})

@api_view(['GET'])
def detect_anomalies(request):
    """API to detect anomalies using Isolation Forest."""
    logs = LogEntry.objects.all().values('level', 'pid')
    df = pd.DataFrame(logs)

    if df.empty:
        return JsonResponse({"message": "No logs available for analysis."})

    from sklearn.ensemble import IsolationForest
    model = IsolationForest(contamination=0.1)
    df['anomaly'] = model.fit_predict(df[['pid']])
    anomalies = df[df['anomaly'] == -1]
    return JsonResponse(anomalies.to_dict(orient='records'), safe=False)