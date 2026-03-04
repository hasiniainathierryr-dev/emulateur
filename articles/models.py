from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=100)              # Nom de l'application
    description = models.TextField(blank=True)           # Description
    version = models.CharField(max_length=20)            # Version (ex: 1.0.3)
    apk_file = models.FileField(upload_to='apks/', blank=True, null=True)  # Fichier APK
    exe_file = models.FileField(upload_to='exe/', blank=True, null=True)   # Fichier EXE
    created_at = models.DateTimeField(auto_now_add=True) # Date d'ajout
    updated_at = models.DateTimeField(auto_now=True)     # Dernière mise à jour

    def __str__(self):
        return f"{self.name} (v{self.version})"
