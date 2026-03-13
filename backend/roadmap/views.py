# from django.shortcuts import render

# # Create your views here.
# import json
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .models import Roadmap, RoadmapStep
# from .ai_service import generate_roadmap_with_ai
# from tasks.models import Task

# from profiles.models import UserProfile


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def generate_roadmap_api(request):
#     user = request.user
#     current_status = request.data.get("current_status")
#     career_goal = request.data.get("career_goal")

#     # ✅ SAVE / UPDATE USER PROFILE
#     profile, created = UserProfile.objects.get_or_create(user=user)
#     profile.current_status = current_status
#     profile.career_goal = career_goal
#     profile.save()

#     # remove old roadmap
#     Roadmap.objects.filter(user=user).delete()

#     # call AI
#     ai_response = generate_roadmap_with_ai(current_status, career_goal)
#     roadmap_data = json.loads(ai_response)

#     roadmap = Roadmap.objects.create(
#         user=user,
#         goal=career_goal
#     )

#     for step in roadmap_data.get("steps", []):
#         roadmap_step = RoadmapStep.objects.create(
#             roadmap=roadmap,
#             step_number=step["step_number"],
#             title=step["title"],
#             description=step["description"],
#             duration=step["duration"]
#         )

#         Task.objects.create(
#             user=user,
#             step=roadmap_step,
#             title=f"Work on: {step['title']}"
#         )
#     print("ready road map")
#     return Response({
#         "message": "AI-generated roadmap created successfully",
#         "total_steps": len(roadmap_data.get("steps", []))
#     })



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_roadmap(request):
#     roadmap = Roadmap.objects.filter(user=request.user).first()

#     if not roadmap:
#         return Response({"message": "No roadmap found"})

#     data = []
#     for step in roadmap.steps.all():
#         data.append({
#             "step_number": step.step_number,
#             "title": step.title,
#             "description": step.description,
#             "duration": step.duration
#         })

#     return Response({
#         "goal": roadmap.goal,
#         "steps": data
#     })


# -------------------- AI SERVICE --------------------
# from django.shortcuts import render
# import json
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .models import Roadmap, RoadmapStep
# from .ai_service import generate_roadmap_with_ai
# from tasks.models import Task
# from profiles.models import UserProfile


# # ---------- FALLBACK TASK GENERATOR ----------
# def generate_default_tasks(step_title):
#     """
#     Used when AI does not return task-level breakdown.
#     Ensures 10+ actionable tasks per step.
#     """
#     return [
#         f"Understand basics of {step_title}",
#         f"Read documentation on {step_title}",
#         f"Watch one tutorial on {step_title}",
#         f"Set up environment for {step_title}",
#         f"Practice core concepts of {step_title}",
#         f"Complete one small exercise on {step_title}",
#         f"Apply {step_title} in a mini example",
#         f"Identify common mistakes in {step_title}",
#         f"Revise key points of {step_title}",
#         f"Summarize learnings from {step_title}"
#     ]


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def generate_roadmap_api(request):
#     user = request.user
#     current_status = request.data.get("current_status")
#     career_goal = request.data.get("career_goal")

#     # ✅ SAVE / UPDATE USER PROFILE
#     profile, _ = UserProfile.objects.get_or_create(user=user)
#     profile.current_status = current_status
#     profile.career_goal = career_goal
#     profile.save()

#     # ✅ REMOVE OLD ROADMAP + TASKS (IMPORTANT)
#     Roadmap.objects.filter(user=user).delete()
#     Task.objects.filter(user=user).delete()

#     # ✅ CALL AI
#     ai_response = generate_roadmap_with_ai(current_status, career_goal)
#     roadmap_data = json.loads(ai_response)

#     roadmap = Roadmap.objects.create(
#         user=user,
#         goal=career_goal
#     )

#     # ✅ CREATE STEPS + MULTIPLE TASKS
#     for step in roadmap_data.get("steps", []):
#         roadmap_step = RoadmapStep.objects.create(
#             roadmap=roadmap,
#             step_number=step.get("step_number"),
#             title=step.get("title"),
#             description=step.get("description"),
#             duration=step.get("duration")
#         )

#         # 1️⃣ If AI provides tasks, use them
#         ai_tasks = step.get("tasks")

#         if ai_tasks and isinstance(ai_tasks, list):
#             task_titles = ai_tasks
#         else:
#             # 2️⃣ Fallback: auto-generate 10+ tasks
#             task_titles = generate_default_tasks(step.get("title"))

#         # 3️⃣ Save each task
#         for task_title in task_titles:
#             Task.objects.create(
#                 user=user,
#                 step=roadmap_step,
#                 title=task_title
#             )

#     return Response({
#         "message": "AI-generated roadmap and tasks created successfully",
#         "total_steps": len(roadmap_data.get("steps", []))
#     })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_roadmap(request):
#     roadmap = Roadmap.objects.filter(user=request.user).first()

#     if not roadmap:
#         return Response({"message": "No roadmap found"})

#     data = []
#     for step in roadmap.steps.all():
#         data.append({
#             "step_number": step.step_number,
#             "title": step.title,
#             "description": step.description,
#             "duration": step.duration
#         })

#     return Response({
#         "goal": roadmap.goal,
#         "steps": data
#     })


# -----------new version with daily tasks -----------
from django.shortcuts import render
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

    # ==============================
    # SAVE / UPDATE USER PROFILE
    # ==============================
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.current_status = current_status
    profile.career_goal = career_goal
    profile.save()

    # ==============================
    # CLEAR OLD DATA (IMPORTANT)
    # ==============================
    Roadmap.objects.filter(user=user).delete()
    Task.objects.filter(user=user).delete()

    # ==============================
    # CALL AI (ROADMAP + TASKS)
    # ==============================
    ai_response = generate_roadmap_with_ai(current_status, career_goal)

    try:
        roadmap_data = json.loads(ai_response)
    except json.JSONDecodeError:
        return Response(
            {"error": "AI returned invalid JSON"},
            status=500
        )

    # ==============================
    # CREATE ROADMAP
    # ==============================
    roadmap = Roadmap.objects.create(
        user=user,
        goal=career_goal
    )

    # ==============================
    # CREATE STEPS + TASKS
    # ==============================
    for step in roadmap_data.get("steps", []):

        roadmap_step = RoadmapStep.objects.create(
            roadmap=roadmap,
            step_number=step.get("step_number"),
            title=step.get("title"),
            description=step.get("description"),
            duration=step.get("duration")
        )

        tasks = step.get("tasks", [])

        # Safety check: AI MUST give tasks
        if not isinstance(tasks, list) or len(tasks) < 5:
            continue  # skip bad AI step safely

        for task_title in tasks:
            Task.objects.create(
                user=user,
                step=roadmap_step,
                title=task_title
            )

    return Response({
        "message": "AI-generated roadmap and tasks created successfully",
        "total_steps": len(roadmap_data.get("steps", []))
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_roadmap(request):
    roadmap = Roadmap.objects.filter(user=request.user).first()

    if not roadmap:
        return Response({"message": "No roadmap found"})

    steps_data = []

    for step in roadmap.steps.all():
        steps_data.append({
            "step_number": step.step_number,
            "title": step.title,
            "description": step.description,
            "duration": step.duration
        })

    return Response({
        "goal": roadmap.goal,
        "steps": steps_data
    })
