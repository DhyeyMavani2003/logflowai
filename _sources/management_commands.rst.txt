Management Commands
===================

LogFlowAI includes several management commands for data ingestion and maintenance.
For example, the `import_logs` command reads log entries from a CSV file and stores them
in the database.

To run the command:

.. code-block:: bash

   python manage.py import_logs

The code for this command is located in the ``logflowai/management/commands/import_logs.py``
file.

.. automodule:: logapp.management.commands.import_logs
    :members:
