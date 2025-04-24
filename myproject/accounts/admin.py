from django.contrib import admin
from .models import AdminUser, NormalUser, Station

admin.site.register(AdminUser)
admin.site.register(NormalUser)
admin.site.register(Station)
