from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="logflow_home"),
    path("dashboard/", views.dashboard, name="logflow_dashboard"),
    path("update_chart/", views.update_chart, name="update_chart"),
    path("import_logs/", views.import_logs, name="logflow_import"),
    path("send_email/", views.send_email, name="logflow_send_email"),
    path(
        "run_orchestrator/",
        views.run_orchestrator,
        name="logflow_run_orchestrator",
    ),
]
