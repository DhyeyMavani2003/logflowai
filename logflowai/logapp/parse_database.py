import re
from datetime import datetime
import pytz
from django.db.models import Count, F
from django.db.models.functions import ExtractHour
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import LogEntry


def filter_logs(
    query="",
    level=None,
    service=None,
    start_date=None,
    end_date=None,
    similarity_threshold=0.1,
):
    """
    Filter logs based on a search query, log level, service, and date range.
    """
    logs = LogEntry.objects.all()

    if level:
        logs = logs.filter(level__iexact=level)
    if service:
        logs = logs.filter(service__iexact=service)
    if start_date and end_date:
        logs = logs.filter(timestamp__date__range=[start_date, end_date])

    if not query:
        return logs.order_by("timestamp").distinct()

    # Exact match on the message
    exact_matches = logs.filter(message__icontains=query)
    log_list = list(
        logs.exclude(id__in=exact_matches.values_list("id", flat=True))
    )
    if not log_list:
        return exact_matches

    messages = [preprocess_text(log.message) for log in log_list]
    processed_query = preprocess_text(query)
    similarity_scores = compute_similarity_scores(processed_query, messages)

    log_scores = [
        (log.id, score)
        for log, score in zip(log_list, similarity_scores)
        if score >= similarity_threshold
    ]

    if not log_scores:
        return exact_matches

    # Combine exact matches (score=1.0) with similarity scores
    from django.db.models import Case, When, FloatField, Value

    exact_scores = [(log.id, 1.0) for log in exact_matches]
    all_scores = exact_scores + log_scores

    score_cases = [
        When(pk=log_id, then=Value(score)) for log_id, score in all_scores
    ]

    return (
        LogEntry.objects.filter(id__in=[log_id for log_id, _ in all_scores])
        .annotate(
            similarity=Case(
                *score_cases,
                default=0.0,
                output_field=FloatField(),
            )
        )
        .order_by("-similarity")
    )


def preprocess_text(text: str) -> str:
    """
    Lowercase, remove special characters, and trim whitespace.
    """
    text = re.sub(r"[^\w\s]", "", text.lower())
    return text.strip()


def compute_similarity_scores(query: str, messages: list) -> list:
    """
    Compute cosine similarity scores between the query and each log message.
    """
    if not query or not messages:
        return [0] * len(messages)

    vectorizer = TfidfVectorizer(stop_words="english")
    all_texts = [query] + messages
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return similarities[0]


def get_logs_by_hour(logs, timezone):
    """
    Group logs by the hour of their timestamp, adjusting to the specified timezone.
    """
    logs_by_hour = (
        logs.exclude(timestamp__isnull=True)
        .annotate(hour=ExtractHour(F("timestamp"), tzinfo=timezone))
        .values("hour")
        .annotate(log_count=Count("id"))
        .order_by("hour")
    )
    return logs_by_hour


def get_unique_services():
    """
    Retrieve a sorted list of unique service names from the logs.
    """
    return LogEntry.objects.values_list("service", flat=True).distinct()
