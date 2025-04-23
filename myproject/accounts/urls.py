from . import views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path("", views.tabelog_index, name="index"),
]
