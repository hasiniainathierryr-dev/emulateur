from django.shortcuts import render
from django.http import JsonResponse
import json
import subprocess
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from articles.models import Application

# --- Pages classiques ---
def startup(request):
    return render(request, "startup.html")

def home(request):
    return render(request, "home.html")

def multitache(request):
    tasks = [
        {"name": "Accueil", "url": "home"},
        {"name": "Paramètres", "url": "parametres"},
        {"name": "Applications", "url": "applications"},
    ]
    return render(request, "multitache.html", {"tasks": tasks})

def parametres(request):
    return render(request, "parametres.html")

def apps(request):
    return render(request, "apps.html", {"apps": Application.objects.all()})


# --- Panneaux réalistes ---
def resolution_page(request):
    return render(request, "resolution.html")

def son_page(request):
    return render(request, "son.html")

def rotation_page(request):
    return render(request, "rotation.html")

def applications_page(request):
    return render(request, "applications.html")


# --- API Waydroid : Clear Disk ---
def clear_disk(request):
    subprocess.run(["waydroid", "session", "wipe"])
    return JsonResponse({"status": "success", "message": "Cache disque nettoyé"})


# --- API Waydroid : Rotation ---
@csrf_exempt
def rotation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        orientation = data.get("orientation")
        subprocess.run(["waydroid", "prop", "set", "persist.sys.display.orientation", orientation])
        return JsonResponse({"status": "success", "orientation": orientation})
    elif request.method == "GET":
        current = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.orientation"],
                                 capture_output=True, text=True).stdout.strip()
        return JsonResponse({"status": "success", "orientation": current})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)


# --- API Waydroid : Résolution ---
@csrf_exempt
def resolution(request):
    if request.method == "POST":
        width = request.POST.get("width")
        height = request.POST.get("height")
        if width: subprocess.run(["waydroid", "prop", "set", "persist.sys.display.width", width])
        if height: subprocess.run(["waydroid", "prop", "set", "persist.sys.display.height", height])
    current_width = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.width"],
                                   capture_output=True, text=True).stdout.strip()
    current_height = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.height"],
                                    capture_output=True, text=True).stdout.strip()
    return JsonResponse({"status": "success", "width": current_width, "height": current_height})

@csrf_exempt
def get_resolution(request):
    if request.method == "GET":
        current_width = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.width"],
                                       capture_output=True, text=True).stdout.strip()
        current_height = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.height"],
                                        capture_output=True, text=True).stdout.strip()
        return JsonResponse({
            "status": "success",
            "message": f"Résolution actuelle : {current_width}x{current_height}",
            "width": current_width,
            "height": current_height
        })
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)


# --- API Waydroid : Affichage (luminosité/contraste) ---
@csrf_exempt
def display(request):
    if request.method == "POST":
        brightness = request.POST.get("brightness")
        contrast = request.POST.get("contrast")
        if brightness:
            subprocess.run(["waydroid", "prop", "set", "persist.sys.display.brightness", brightness])
        if contrast:
            subprocess.run(["waydroid", "prop", "set", "persist.sys.display.contrast", contrast])
    current_brightness = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.brightness"],
                                        capture_output=True, text=True).stdout.strip()
    current_contrast = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.contrast"],
                                      capture_output=True, text=True).stdout.strip()
    return JsonResponse({"status": "success", "brightness": current_brightness, "contrast": current_contrast})

@csrf_exempt
def get_display(request):
    if request.method == "GET":
        current_brightness = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.brightness"],
                                            capture_output=True, text=True).stdout.strip()
        current_contrast = subprocess.run(["waydroid", "prop", "get", "persist.sys.display.contrast"],
                                          capture_output=True, text=True).stdout.strip()
        return JsonResponse({
            "status": "success",
            "message": f"Luminosité {current_brightness}% - Contraste {current_contrast}%",
            "brightness": current_brightness,
            "contrast": current_contrast
        })
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)


# --- API Waydroid : Son ---
@csrf_exempt
def sound(request):
    if request.method == "POST":
        volume = request.POST.get("volume")
        mode = request.POST.get("mode")
        if volume: subprocess.run(["waydroid", "prop", "set", "persist.sys.audio.volume", volume])
        if mode: subprocess.run(["waydroid", "prop", "set", "persist.sys.audio.mode", mode])
    current_volume = subprocess.run(["waydroid", "prop", "get", "persist.sys.audio.volume"],
                                    capture_output=True, text=True).stdout.strip()
    current_mode = subprocess.run(["waydroid", "prop", "get", "persist.sys.audio.mode"],
                                  capture_output=True, text=True).stdout.strip()
    return JsonResponse({"status": "success", "volume": current_volume, "mode": current_mode})

@csrf_exempt
def get_sound(request):
    if request.method == "GET":
        current_volume = subprocess.run(["waydroid", "prop", "get", "persist.sys.audio.volume"],
                                        capture_output=True, text=True).stdout.strip()
        current_mode = subprocess.run(["waydroid", "prop", "get", "persist.sys.audio.mode"],
                                      capture_output=True, text=True).stdout.strip()
        return JsonResponse({"status": "success", "volume": current_volume, "mode": current_mode})
    return JsonResponse({"status": "error", "message": "Méthode non supportée"}, status=405)


# --- API Waydroid : CPU & RAM ---
@csrf_exempt
def set_cpu(request):
    cores = request.POST.get("cores")
    if cores: subprocess.run(["waydroid", "prop", "set", "persist.sys.cpu.cores", cores])
    current = subprocess.run(["waydroid", "prop", "get", "persist.sys.cpu.cores"],
                             capture_output=True, text=True).stdout.strip()
    return JsonResponse({"status": "success", "cores": current})

@csrf_exempt
def set_ram(request):
    ram = request.POST.get("ram")
    if ram: subprocess.run(["waydroid", "prop", "set", "persist.sys.memory.ram", ram])
    current = subprocess.run(["waydroid", "prop", "get", "persist.sys.memory.ram"],
                             capture_output=True, text=True).stdout.strip()
    return JsonResponse({"status": "success", "ram": current})


# --- Applications ---
@csrf_exempt
def list_apps(request):
    apps = Application.objects.all()
    data = [{"id": app.id, "name": app.name, "package": app.package} for app in apps]
    return JsonResponse({"apps": data})

@csrf_exempt
def open_app(request, package):
    subprocess.run(["waydroid", "app", "launch", package])
    return JsonResponse({"status": "success", "message": f"Application '{package}' ouverte"})

@csrf_exempt
def delete_app(request, app_id):
    try:
        app = Application.objects.get(id=app_id)
        app.delete()
        return JsonResponse({"status": "success", "message": f"Application '{app.name}' supprimée"})
    except Application.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Application introuvable"}, status=404)


# --- API REST de test ---
@api_view(["GET"])
def test_api(request):
    return Response({"message": "Hello depuis Django"})
