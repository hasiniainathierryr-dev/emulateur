from django.urls import path
from dashboard.views import clear_disk, rotate, resolution, sound, test_api

urlpatterns = [
    path("test/", test_api, name="test_api"),
    path("waydroid/clear/", clear_disk, name="waydroid_clear"),
    path("waydroid/rotate/", rotate, name="waydroid_rotate"),
    path("waydroid/resolution/", resolution, name="waydroid_resolution"),
    path("waydroid/sound/", sound, name="waydroid_sound"),
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- Pages classiques ---
    path("", include("dashboard.urls")),
    path("articles/", include("articles.urls")),

    # --- API Waydroid ---
    path("api/test/", views.test_api, name="test_api"),
    path("api/waydroid/clear/", views.clear_disk, name="waydroid_clear"),

    # Rotation
    path("api/waydroid/rotation/", views.rotation, name="waydroid_rotation"),

    # Résolution & Affichage
    path("api/waydroid/resolution/", views.resolution, name="waydroid_resolution"),
    path("api/waydroid/display/", views.display, name="waydroid_display"),
    path("api/waydroid/display/get/", views.get_display, name="get_display"),

    # Son
    path("api/waydroid/sound/", views.sound, name="waydroid_sound"),
    path("api/waydroid/sound/get/", views.get_sound, name="get_sound"),

    # CPU & RAM
    path("api/waydroid/cpu/", views.set_cpu, name="waydroid_cpu"),
    path("api/waydroid/ram/", views.set_ram, name="waydroid_ram"),

    # Applications
    path("api/waydroid/apps/", views.list_apps, name="waydroid_apps"),

    # Nouveau réglage indépendant : Mode Performance
    path("api/waydroid/performance/", views.performance_mode, name="waydroid_performance"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
