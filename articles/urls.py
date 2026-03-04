from django.urls import path
from . import views

urlpatterns = [
    # API ou pages reliées aux applications
    path('apps/', views.apps, name='apps'),  # ✅ correspond à ta vue apps dans views.py
]
