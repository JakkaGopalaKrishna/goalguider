from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from profiles.models import UserProfile

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response(
        {"message": "User registered successfully"},
        status=status.HTTP_201_CREATED
    )


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def me(request):
#     user = request.user
#     return Response({
#         "id": user.id,
#         "username": user.username,
#         "email": user.email
#     })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    # Try to get profile (may not exist yet)
    profile = UserProfile.objects.filter(user=user).first()

    return Response({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined
        },
        "current_status": profile.current_status if profile else None,
        "career_goal": profile.career_goal if profile else None
    })
