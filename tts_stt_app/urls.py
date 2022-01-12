from django.urls import path, include
from . import views

urlpatterns = [
    path('spell_check',views.main_spell_check),
]
