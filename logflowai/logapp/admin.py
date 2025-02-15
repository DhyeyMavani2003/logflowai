from django.contrib import admin
from .models import LogEntry
 
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('line_id', 'date', 'time', 'level', 'component', 'content')
    search_fields = ('level', 'component', 'content')
    list_filter = ('level', 'date')

admin.site.site_header = "LogFlowAI Admin"