Database Parsing and Analysis
===============================

This module provides functionality for filtering, processing, and analyzing log data.
Key functions include:

- **filter_logs**: Filter logs based on query, level, service, and date range, with both
  exact and fuzzy matching.
- **preprocess_text**: Normalize text by lowercasing and removing special characters.
- **compute_similarity_scores**: Compute cosine similarity between a query and log messages.
- **get_logs_by_hour**: Group log entries by the hour of their timestamp.
- **get_unique_services**: Retrieve a list of unique service names from log entries.

.. automodule:: logapp.parse_database
    :members:
