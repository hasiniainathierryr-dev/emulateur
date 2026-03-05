from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Application
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser le message d'erreur pour username
        self.fields["username"].error_messages = {
            "unique": "Ce nom est déjà pris, choisis-en un autre 😉",
            "required": "Le nom d’utilisateur est obligatoire."
        }
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "package", "version", "description", "apk_file", "exe_file"]