Welcome to LogFlowAI's Documentation!
=======================================

LogFlowAI is a real-time log analysis and monitoring platform. It ingests,
filters, and visualizes log data to help teams diagnose issues and monitor
system performance efficiently.

Overview
========

LogFlowAI provides:
- **Real-time Log Ingestion:** Import and process log data from CSV files and other sources.
- **Advanced Filtering:** Search logs by query, level, service, or date range.
- **Dashboard Visualizations:** See aggregated metrics such as logs per hour and unique service statistics.
- **Extensible API:** Easily extend and integrate log analysis with your existing systems.

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