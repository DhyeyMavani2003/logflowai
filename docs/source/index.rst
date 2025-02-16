Welcome to LogFlowAI's Documentation!
=======================================
LogFlowAI is an enterprise-grade platform for real-time log analysis and monitoring, designed to handle massive log volumes across distributed systems. Our platform empowers engineering teams with advanced tools for log ingestion, intelligent analysis, and interactive visualizations to maintain optimal system performance and quickly diagnose issues.

Overview
========

- **Real-time Log Ingestion:** Stream and process logs from diverse sources including CSV files, syslog streams, JSON endpoints, and Kubernetes logs. Support both batch processing for historical data and real-time streaming with sub-second latency. Automatically handle data validation, field extraction, and timestamp normalization across multiple timezones.
- **Advanced Filtering:** Power through millions of log entries with our sophisticated search capabilities. Combine full-text search, regex patterns, and field-specific filters to pinpoint exactly what you need. Features include fuzzy matching, saved searches, query templates, and support for complex boolean operations across log level, service name, timestamp, and custom fields.
- **Dashboard Visualizations:** Transform raw logs into actionable insights with our interactive dashboards. Track key metrics like error rates and service health in real-time, visualize log patterns with heat maps and time-series graphs, and create custom views for different teams. All visualizations support drill-down capabilities and export options for deeper analysis.
- **Extensible API:** Seamlessly integrate LogFlowAI into your existing infrastructure through our comprehensive RESTful API. Ingest logs programmatically, trigger automated analyses, and export metrics to external systems. The API includes robust authentication, rate limiting, detailed documentation, and support for custom plugins to extend functionality.

Getting Started
===============

To clone and set up the application locally, run the following commands:

.. code-block:: bash

   git clone https://github.com/DhyeyMavani2003/logflowai.git
   cd logflowai

Create and activate a virtual environment:

.. code-block:: bash

   python3 -m venv env
   source env/bin/activate

Install dependencies:

.. code-block:: bash

   pip install -r requirements.txt

Apply database migrations:

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate

To start the development server, run:

.. code-block:: bash

   python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser to view the application.

Contents
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   log_entry_model
   parse_database
   management_commands
   api_endpoints

Additional Resources
====================

For more information on contributing, reporting issues, or requesting features, please visit our
[GitHub repository](https://github.com/DhyeyMavani2003/logflowai).