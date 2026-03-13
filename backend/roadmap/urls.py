from django.urls import path
from .views import generate_roadmap_api, get_roadmap

urlpatterns = [
    path('generate/', generate_roadmap_api),
    path('', get_roadmap),
]
