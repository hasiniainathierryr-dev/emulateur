from django.urls import path
from dashboard import views

urlpatterns = [
    # --- Pages classiques ---
    path("", views.startup, name="startup"),
    path("home/", views.home, name="home"),
    path("multitache/", views.multitache, name="multitache"),
    path("parametres/", views.parametres, name="parametres"),
    path("apps/", views.apps, name="apps"),

    # --- Nouveaux panneaux réalistes ---
    path("rotation/", views.rotation_page, name="rotation"),
    path("resolution/", views.resolution_page, name="resolution"),
    path("son/", views.son_page, name="son"),
    path("applications/", views.applications_page, name="applications"),

    # --- API Waydroid ---
    path("api/waydroid/clear_disk/", views.clear_disk, name="clear_disk"),

    # Résolution
    path("api/waydroid/resolution/", views.resolution, name="api_resolution"),
    path("api/waydroid/get_resolution/", views.get_resolution, name="api_get_resolution"),

    # Affichage (luminosité/contraste)
    path("api/waydroid/display/", views.display, name="api_display"),
    path("api/waydroid/get_display/", views.get_display, name="api_get_display"),

    # Rotation
    path("api/waydroid/rotation/", views.rotation, name="api_rotation"),

    # Son
    path("api/waydroid/sound/", views.sound, name="api_sound"),
    path("api/waydroid/get_sound/", views.get_sound, name="api_get_sound"),

    # CPU & RAM
    path("api/waydroid/cpu/", views.set_cpu, name="api_cpu"),
    path("api/waydroid/ram/", views.set_ram, name="api_ram"),

    # Applications
    path("api/waydroid/apps/", views.list_apps, name="api_list_apps"),
    path("api/waydroid/open_app/<str:package>/", views.open_app, name="api_open_app"),
    path("api/waydroid/delete_app/<int:app_id>/", views.delete_app, name="api_delete_app"),

    # --- API REST de test ---
    path("api/test/", views.test_api, name="test_api"),
]
