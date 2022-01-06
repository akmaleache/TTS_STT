from django.urls import path, include
from . import views

urlpatterns = [
    path('cognitive/STT',views.main_stt),
    path('cognitive/TTS',views.main_tts),
]
