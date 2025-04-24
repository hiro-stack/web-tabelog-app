from . import views
from django.urls import path
import uuid

app_name = "accounts"

urlpatterns = [
    path("", views.admin_create, name="index"),
    path("list/", views.admin_list, name="list"),
    path("user/add/<uuid:admin_id>/", views.normal_create, name="add_user"),
    path("station/add/<uuid:admin_id>/", views.station_create, name="add_station"),
]
