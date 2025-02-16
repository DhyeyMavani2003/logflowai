from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from dateutil import parser
from datetime import timedelta
import json
import pytz
from django.core.management import call_command
from .models import LogEntry
from .parse_database import filter_logs, get_logs_by_hour, get_unique_services


@csrf_exempt
def import_logs(request):
    """
    Trigger the import_logs management command to load log data from CSV.
    """
    if request.method == "POST":
        try:
            call_command("import_logs")
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse(
        {"status": "error", "message": "POST request required."}, status=400
    )


@csrf_exempt
def send_email(request):
    """
    Trigger the send_email management command to send an email via Outlook.
    """
    if request.method == "POST":
        try:
            call_command("execute_scrapybara_email")
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse(
        {"status": "error", "message": "POST request required."}, status=400
    )


@csrf_exempt
def run_orchestrator(request):
    """
    Trigger the run_orchestrator management command to execute the LangGraph orchestrator.
    """
    if request.method == "POST":
        try:
            call_command("run_orchestrator")
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse(
        {"status": "error", "message": "POST request required."}, status=400
    )


def home(request):
    """
    Render the home page with filters to search and display log entries.
    """
    query = request.GET.get("query", "")
    level = request.GET.get("level", None)
    service = request.GET.get("service", None)

    # Default date range: past  days
    today = timezone.now().date()
    default_start = (today - timedelta(days=7, weeks=52*25)).isoformat()
    default_end = today.isoformat()

    start_date = request.GET.get("start_date", default_start)
    end_date = request.GET.get("end_date", default_end)

    start_date_obj = parser.parse(start_date).date()
    end_date_obj = parser.parse(end_date).date()

    logs = filter_logs(
        query=query,
        level=level,
        service=service,
        start_date=start_date_obj,
        end_date=end_date_obj,
    )

    # Group logs by date
    logs_by_date = {}
    for log in logs:
        # Only include logs with a valid timestamp
        if log.timestamp:
            log_date = log.timestamp.astimezone(pytz.UTC).date()
            logs_by_date.setdefault(log_date, []).append(log)

    # Sort each group by timestamp
    for date_key in logs_by_date:
        logs_by_date[date_key].sort(key=lambda x: x.timestamp)

    context = {
        "logs_by_date": logs_by_date,
        "query": query,
        "level": level,
        "service": service,
        "start_date": start_date_obj.isoformat(),
        "end_date": end_date_obj.isoformat(),
        "unique_services": get_unique_services(),
    }
    return render(request, "logapp/home.html", context)


def dashboard(request):
    """
    Render a dashboard view with log insights such as logs per hour.
    """
    tz = pytz.timezone("UTC")
    logs = LogEntry.objects.all()

    context = {
        "logs_by_hour": get_logs_by_hour(logs, tz),
    }
    return render(request, "logapp/dashboard.html", context)


@csrf_exempt
def update_chart(request):
    """
    Update the log chart based on a specified hour range.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        min_hour = data.get("min_hour", 0)
        max_hour = data.get("max_hour", 23)

        tz = pytz.timezone("UTC")
        logs = LogEntry.objects.all().exclude(timestamp__isnull=True)
        filtered_logs = logs.filter(
            timestamp__hour__gte=min_hour, timestamp__hour__lte=max_hour
        )
        logs_by_hour = get_logs_by_hour(filtered_logs, tz)

        return JsonResponse({"logs_by_hour": list(logs_by_hour)})

    return JsonResponse({"error": "Invalid request method"}, status=400)
