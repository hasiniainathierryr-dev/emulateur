from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import subprocess
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from articles.models import Application
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import UserSettings
from django.shortcuts import render, redirect
from .models import Application
from .forms import ApplicationForm
# --- Pages classiques ---
def startup(request):
    # Seul startup.html est dans dashboard/templates/dashboard/
    return render(request, "dashboard/startup.html")

def home(request):
    return render(request, "home.html")

def multitache(request):
    tasks = [
        {"name": "Accueil", "url": "home"},
        {"name": "Paramètres", "url": "parametres"},
        {"name": "Applications", "url": "applications_page"},
    ]
    return render(request, "multitache.html", {"tasks": tasks})

def parametres(request):
    return render(request, "parametres.html")

def apps(request):
    return render(request, "apps.html", {"apps": Application.objects.all()})


# --- Panneaux réalistes (simulation persistante) ---
def resolution_page(request):
    resolution = request.session.get("resolution", "1024x768")
    brightness = request.session.get("brightness", "100")
    contrast = request.session.get("contrast", "100")

    if request.method == "POST":
        resolution = request.POST.get("resolution", resolution)
        brightness = request.POST.get("brightness", brightness)
        contrast = request.POST.get("contrast", contrast)

        request.session["resolution"] = resolution
        request.session["brightness"] = brightness
        request.session["contrast"] = contrast

        return redirect("resolution_page")

    context = {"resolution": resolution, "brightness": brightness, "contrast": contrast}
    return render(request, "resolution.html", context)

def son_page(request):
    volume = request.session.get("volume", "50")
    mode = request.session.get("mode", "normal")

    if request.method == "POST":
        volume = request.POST.get("volume", volume)
        mode = request.POST.get("mode", mode)
        request.session["volume"] = volume
        request.session["mode"] = mode
        return redirect("son_page")

    context = {"volume": volume, "mode": mode}
    return render(request, "son.html", context)

def rotation_page(request):
    orientation = request.session.get("orientation", "portrait")

    if request.method == "POST":
        orientation = request.POST.get("orientation", orientation)
        request.session["orientation"] = orientation
        return redirect("rotation_page")

    context = {"orientation": orientation}
    return render(request, "rotation.html", context)

def applications_page(request):
    return render(request, "applications.html")


# --- API simulées (sessions Django au lieu de Waydroid) ---
@csrf_exempt
def display(request):
    if request.method == "POST":
        brightness = request.POST.get("brightness")
        contrast = request.POST.get("contrast")
        request.session["brightness"] = brightness
        request.session["contrast"] = contrast
        return JsonResponse({"status": "success", "message": "Réglages appliqués"})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)

@csrf_exempt
def get_display(request):
    if request.method == "GET":
        brightness = request.session.get("brightness", "100")
        contrast = request.session.get("contrast", "100")
        return JsonResponse({
            "status": "success",
            "message": f"Luminosité {brightness}% - Contraste {contrast}%",
            "brightness": brightness,
            "contrast": contrast
        })
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)

@csrf_exempt
def sound(request):
    if request.method == "POST":
        volume = request.POST.get("volume")
        mode = request.POST.get("mode")
        request.session["volume"] = volume
        request.session["mode"] = mode
        return JsonResponse({"status": "success", "message": "Réglages son appliqués"})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)

@csrf_exempt
def get_sound(request):
    if request.method == "GET":
        volume = request.session.get("volume", "50")
        mode = request.session.get("mode", "normal")
        return JsonResponse({"status": "success", "volume": volume, "mode": mode})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)

@csrf_exempt
def set_cpu(request):
    if request.method == "POST":
        cores = request.POST.get("cores")
        request.session["cpu_cores"] = cores
        return JsonResponse({"status": "success", "message": f"CPU réglé à {cores} cœurs"})
    current = request.session.get("cpu_cores", "2")
    return JsonResponse({"status": "success", "cores": current})

@csrf_exempt
def set_ram(request):
    if request.method == "POST":
        ram = request.POST.get("ram")
        request.session["ram"] = ram
        return JsonResponse({"status": "success", "message": f"RAM réglée à {ram} Mo"})
    current = request.session.get("ram", "2048")
    return JsonResponse({"status": "success", "ram": current})


# --- API Waydroid (⚠️ fonctionne seulement en local Linux avec Waydroid installé) ---
def clear_disk(request):
    subprocess.run(["waydroid", "session", "wipe"])
    return JsonResponse({"status": "success", "message": "Cache disque nettoyé"})

@csrf_exempt
def rotation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        orientation = data.get("orientation")
        subprocess.run(["waydroid", "prop", "set", "persist.sys.display.orientation", orientation])
        return JsonResponse({"status": "success", "orientation": orientation})
    elif request.method == "GET":
        current = subprocess.run(
            ["waydroid", "prop", "get", "persist.sys.display.orientation"],
            capture_output=True, text=True
        ).stdout.strip()
        return JsonResponse({"status": "success", "orientation": current})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

@csrf_exempt
def resolution(request):
    if request.method == "POST":
        width = request.POST.get("width")
        height = request.POST.get("height")
        if width:
            subprocess.run(["waydroid", "prop", "set", "persist.sys.display.width", width])
        if height:
            subprocess.run(["waydroid", "prop", "set", "persist.sys.display.height", height])
    current_width = subprocess.run(
        ["waydroid", "prop", "get", "persist.sys.display.width"],
        capture_output=True, text=True
    ).stdout.strip()
    current_height = subprocess.run(
        ["waydroid", "prop", "get", "persist.sys.display.height"],
        capture_output=True, text=True
    ).stdout.strip()
    return JsonResponse({"status": "success", "width": current_width, "height": current_height})

@csrf_exempt
def get_resolution(request):
    if request.method == "GET":
        current_width = subprocess.run(
            ["waydroid", "prop", "get", "persist.sys.display.width"],
            capture_output=True, text=True
        ).stdout.strip()
        current_height = subprocess.run(
            ["waydroid", "prop", "get", "persist.sys.display.height"],
            capture_output=True, text=True
        ).stdout.strip()
        return JsonResponse({
            "status": "success",
            "message": f"Résolution actuelle : {current_width}x{current_height}",
            "width": current_width,
            "height": current_height
        })
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)


# --- Gestion des applications ---
@csrf_exempt
def list_apps(request):
    if request.method == "GET":
        apps = Application.objects.all().values("id", "name", "version", "description")
        return JsonResponse({"status": "success", "apps": list(apps)})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)
def add_app(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("apps")  # retourne vers la liste
    else:
        form = ApplicationForm()
    return render(request, "add_app.html", {"form": form})

@csrf_exempt
def open_app(request, package):
    if request.method == "POST":
        return JsonResponse({"status": "success", "message": f"Application {package} ouverte"})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)

@csrf_exempt
def delete_app(request, app_id):
    if request.method == "DELETE":
        app = get_object_or_404(Application, id=app_id)
        app.delete()
        return JsonResponse({"status": "success", "message": f"Application {app.name} supprimée"})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)


# --- Authentification ---
def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserSettings.objects.create(user=user)
            login(request, user)
            return redirect("profile")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            return render(request, "login.html", {"error": "Identifiants invalides"})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    settings = UserSettings.objects.get(user=request.user)
    return render(request, "profile.html", {"settings": settings})

def landing_view(request):
    return render(request, "landing.html")

def tutorial_view(request):
    return render(request, "tutorial.html")

# --- API REST de test ---
@api_view(["GET"])
def test_api(request):
    return Response({"message": "Hello depuis Django"})
