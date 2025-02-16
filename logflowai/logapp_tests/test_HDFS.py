import pytest
import json
from datetime import timedelta
import pytz
from django.utils import timezone
from django.db.models import QuerySet
from logapp.models import LogEntry
from logapp.parse_database import (
    filter_logs,
    preprocess_text,
    compute_similarity_scores,
    get_logs_by_hour,
    get_unique_services,
)

# ---------------------------------
# Tests for preprocess_text and compute_similarity_scores
# ---------------------------------


def test_preprocess_text():
    text = "  Hello, World!  "
    expected = "hello world"
    assert preprocess_text(text) == expected


def test_compute_similarity_scores_empty():
    scores = compute_similarity_scores("", ["anything", "else"])
    assert scores == [0, 0]


def test_compute_similarity_scores_similarity():
    query = "system startup complete"
    messages = ["System startup complete", "different text"]
    scores = compute_similarity_scores(
        preprocess_text(query), [preprocess_text(m) for m in messages]
    )
    assert scores[0] > 0.9
    assert scores[1] < 0.5


# ---------------------------------
# Fixtures for creating LogEntry instances
# ---------------------------------


@pytest.fixture
def create_log_entries(db):
    now = timezone.now()
    LogEntry.objects.create(
        timestamp=now - timedelta(hours=2),
        level="INFO",
        message="System startup complete",
        service="CoreService",
        host="host1",
        additional_data={"detail": "init complete"},
    )
    LogEntry.objects.create(
        timestamp=now - timedelta(hours=1),
        level="WARNING",
        message="High memory usage detected",
        service="MonitorService",
        host="host2",
        additional_data={"detail": "usage 90%"},
    )
    LogEntry.objects.create(
        timestamp=now,
        level="ERROR",
        message="Service crash reported",
        service="CoreService",
        host="host3",
        additional_data={"detail": "crash code 500"},
    )


@pytest.fixture
def log_factory(db):
    def create_log(**kwargs):
        return LogEntry.objects.create(
            timestamp=kwargs.get("timestamp", timezone.now()),
            level=kwargs.get("level", "INFO"),
            message=kwargs.get("message", "Test log message"),
            service=kwargs.get("service", "TestService"),
            host=kwargs.get("host", "TestHost"),
            additional_data=kwargs.get("additional_data", None),
        )

    return create_log


# ---------------------------------
# Tests for filter_logs
# ---------------------------------


@pytest.mark.django_db
def test_filter_logs_no_query(create_log_entries):
    qs = filter_logs()
    assert qs.count() == 3
    timestamps = list(qs.values_list("timestamp", flat=True))
    assert timestamps == sorted(timestamps)


@pytest.mark.django_db
def test_filter_logs_exact_match(create_log_entries):
    qs = filter_logs(query="System startup complete")
    # We expect at least one log with a matching message.
    assert qs.count() >= 1
    exact = qs.filter(message__icontains="System startup complete").first()
    assert exact is not None
    # If the returned log has a "similarity" attribute, then it should be 1.0.
    # Otherwise, assume that exact matches are unannotated and implicitly 1.0.
    if hasattr(exact, "similarity"):
        assert exact.similarity == 1.0


@pytest.mark.django_db
def test_filter_logs_with_level_and_service(log_factory):
    log_factory(level="INFO", service="AService", message="Alpha event")
    log_factory(level="ERROR", service="BService", message="Beta event")
    log_factory(level="INFO", service="AService", message="Gamma event")

    qs = filter_logs(level="INFO", service="AService")
    for log in qs:
        assert log.level == "INFO"
        assert log.service == "AService"
    messages = [log.message for log in qs]
    assert "Alpha event" in messages
    assert "Gamma event" in messages
    assert "Beta event" not in messages


@pytest.mark.django_db
def test_filter_logs_date_range(log_factory):
    now = timezone.now()
    past = now - timedelta(days=10)
    future = now + timedelta(days=10)
    log_factory(timestamp=past, message="Past event")
    log_factory(timestamp=now, message="Current event")
    log_factory(timestamp=future, message="Future event")

    qs = filter_logs(start_date=past.date(), end_date=now.date())
    messages = [log.message for log in qs]
    assert "Past event" in messages
    assert "Current event" in messages
    assert "Future event" not in messages


@pytest.mark.django_db
def test_filter_logs_similarity(log_factory):
    log_factory(message="Database connection established", service="DBService")
    log_factory(message="database connection established", service="DBService")
    log_factory(message="Network timeout error", service="NetService")

    qs = filter_logs(
        query="Database connection established", similarity_threshold=0.1
    )
    messages = [log.message for log in qs]
    assert any("Database connection established" in msg for msg in messages)
    assert all("timeout" not in msg.lower() for msg in messages)


# ---------------------------------
# Tests for get_logs_by_hour
# ---------------------------------


@pytest.mark.django_db
def test_get_logs_by_hour(log_factory):
    tz = pytz.timezone("UTC")
    now = timezone.now().astimezone(tz)
    log_factory(timestamp=now.replace(hour=8), message="Morning log")
    log_factory(
        timestamp=now.replace(hour=8, minute=30), message="Another morning log"
    )
    log_factory(timestamp=now.replace(hour=15), message="Afternoon log")

    qs = LogEntry.objects.all()
    grouped = get_logs_by_hour(qs, tz)
    hours = [group["hour"] for group in grouped]
    assert 8 in hours
    assert 15 in hours
    for group in grouped:
        if group["hour"] == 8:
            assert group["log_count"] == 2


# ---------------------------------
# Tests for get_unique_services
# ---------------------------------


@pytest.mark.django_db
def test_get_unique_services(log_factory):
    log_factory(service="ServiceA", message="Log A")
    log_factory(service="ServiceB", message="Log B")
    log_factory(service="ServiceA", message="Another log A")

    unique_services = list(get_unique_services())
    assert isinstance(unique_services, list)
    assert "ServiceA" in unique_services
    assert "ServiceB" in unique_services
    # If only these services exist in a clean DB, count should be 2.
    # Note: if other logs exist, this may be >2.
