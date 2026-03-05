from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=20, default="1024x768")
    brightness = models.IntegerField(default=100)
    contrast = models.IntegerField(default=100)
    orientation = models.CharField(max_length=20, default="portrait")
    volume = models.IntegerField(default=50)
    mode = models.CharField(max_length=20, default="normal")

    class Meta:
        verbose_name = "Paramètre utilisateur"
        verbose_name_plural = "Paramètres utilisateurs"

    def __str__(self):
        return f"Paramètres de {self.user.username}"


class Application(models.Model):
    name = models.CharField(max_length=100)
    package = models.CharField(max_length=100, unique=True)  # ⚠️ obligatoire
    version = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    apk_file = models.FileField(upload_to="apps/apk/", blank=True, null=True)
    exe_file = models.FileField(upload_to="apps/exe/", blank=True, null=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return f"{self.name} ({self.package})"
