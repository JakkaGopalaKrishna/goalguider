from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import register, me

urlpatterns = [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/', me),
]
