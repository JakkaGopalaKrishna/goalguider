from django.shortcuts import render

# Create your views here.
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Roadmap, RoadmapStep
from .ai_service import generate_roadmap_with_ai
from tasks.models import Task

from profiles.models import UserProfile


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_roadmap_api(request):
    user = request.user
    current_status = request.data.get("current_status")
    career_goal = request.data.get("career_goal")

    # ✅ SAVE / UPDATE USER PROFILE
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.current_status = current_status
    profile.career_goal = career_goal
    profile.save()

    # remove old roadmap
    Roadmap.objects.filter(user=user).delete()

    # call AI
    ai_response = generate_roadmap_with_ai(current_status, career_goal)
    roadmap_data = json.loads(ai_response)

    roadmap = Roadmap.objects.create(
        user=user,
        goal=career_goal
    )

    for step in roadmap_data.get("steps", []):
        roadmap_step = RoadmapStep.objects.create(
            roadmap=roadmap,
            step_number=step["step_number"],
            title=step["title"],
            description=step["description"],
            duration=step["duration"]
        )

        Task.objects.create(
            user=user,
            step=roadmap_step,
            title=f"Work on: {step['title']}"
        )
    print("ready road map")
    return Response({
        "message": "AI-generated roadmap created successfully",
        "total_steps": len(roadmap_data.get("steps", []))
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_roadmap(request):
    roadmap = Roadmap.objects.filter(user=request.user).first()

    if not roadmap:
        return Response({"message": "No roadmap found"})

    data = []
    for step in roadmap.steps.all():
        data.append({
            "step_number": step.step_number,
            "title": step.title,
            "description": step.description,
            "duration": step.duration
        })

    return Response({
        "goal": roadmap.goal,
        "steps": data
    })
