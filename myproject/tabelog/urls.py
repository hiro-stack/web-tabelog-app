from . import views
from django.urls import path
import uuid

app_name = "tabelog"

urlpatterns = [
    path("<uuid:admin_id>", views.tabelog_index, name="index"),
    path("confirm/<uuid:admin_id>", views.tabelog_confirm, name="confirm"),
    path(
        "confirm/<uuid:admin_id>/execution", views.tabelog_execution, name="execution"
    ),
]
