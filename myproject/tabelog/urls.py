from . import views
from django.urls import path

app_name = "tabelog"

urlpatterns = [
    path("", views.tabelog_index, name="index"),
]
