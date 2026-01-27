from django.urls import path
from .views import complete_task, get_tasks, get_streak

urlpatterns = [
    path('', get_tasks),
    path('complete/', complete_task),
    path('streak/', get_streak),
]
