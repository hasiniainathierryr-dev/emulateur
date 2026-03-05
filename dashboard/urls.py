from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    # --- Administration ---
    path("admin/", admin.site.urls),
    #path("", include("dashboard.urls")),

    # --- Landing page (page vitrine) ---
    path("", views.landing_view, name="landing"),

    # --- Pages classiques ---
    path("startup/", views.startup, name="startup"),  # startup.html dans dashboard/templates/dashboard/
    path("home/", views.home, name="home"),
    path("multitache/", views.multitache, name="multitache"),
    path("parametres/", views.parametres, name="parametres"),
    path("apps/", views.apps, name="apps"),

    # --- Panneaux réalistes (pages utilisateur) ---
    path("rotation/", views.rotation_page, name="rotation_page"),
    path("resolution/", views.resolution_page, name="resolution_page"),
    path("son/", views.son_page, name="son_page"),
    path("applications/", views.applications_page, name="applications_page"),

    # --- API Waydroid simulées ---
    path("api/waydroid/clear_disk/", views.clear_disk, name="api_clear_disk"),

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

    # --- Authentification ---
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("apps/add/", views.add_app, name="add_app"),


    # --- Tutoriel / Démo ---
    path("tutorial/", views.tutorial_view, name="tutorial"),
]
