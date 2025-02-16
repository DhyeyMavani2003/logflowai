# LogFlowAI Backend Documentation Guide

This guide walks you through adding documentation to LogFlowAI with Sphinx.

## Prerequisites

Ensure you have the following installed in your project environment:

- Sphinx
- Django

You can install Sphinx with:

```bash
pip install sphinx
```

## Adding Documentation for Models

You can document your Django models (or other code) using Sphinx. Here’s an example using the `LogEntry` model:

```python
# models.py
from django.db import models

class LogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    service_name = models.CharField(max_length=255)
    log_level = models.CharField(max_length=50)
    message = models.TextField()
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.service_name} - {self.log_level}"
```

## Creating a `.rst` File for the Model

1. **Create an `.rst` file** in `docs/source/` for the model, e.g., `log_entry_model.rst`:

   ```rst
   LogEntry Model
   ==============

   .. automodule:: logflowai.models
       :members: LogEntry
   ```

2. **Update the `index.rst` file** to include the new `.rst` file:

   ```rst
   .. toctree::
       :maxdepth: 2
       :caption: Contents:

       log_entry_model
   ```

3. **Rebuild the HTML documentation** by running:

   ```bash
   make html
   ```

## Viewing the Documentation

Each piece of documentation has its own corresponding `.html` file that can be viewed:

- **Locally**: Navigate to `build/html/index.html` in your file system and open it in a browser.
- **In Gitpod**: Use the following command to preview it:
  ```bash
  gp preview $(pwd)/build/html/index.html
  ```