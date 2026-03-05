from django.contrib import admin
from django.urls import path, include   # ⚠️ ajoute include ici

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),  # ✅ fonctionne maintenant
]
