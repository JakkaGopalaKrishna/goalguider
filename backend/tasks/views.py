from django.shortcuts import render

# Create your views here.
from datetime import date, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task, Streak

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_task(request):
    user = request.user
    task_id = request.data.get("task_id")

    try:
        task = Task.objects.get(id=task_id, user=user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    if task.is_completed:
        return Response({"message": "Task already completed"})

    # Mark task complete
    task.is_completed = True
    task.completed_at = date.today()
    task.save()

    # Handle streak
    streak, created = Streak.objects.get_or_create(user=user)

    today = date.today()

    if streak.last_completed_date == today:
        pass  # already counted today
    elif streak.last_completed_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1

    streak.last_completed_date = today

    if streak.current_streak > streak.best_streak:
        streak.best_streak = streak.current_streak

    streak.save()

    return Response({
        "message": "Task completed successfully",
        "current_streak": streak.current_streak,
        "best_streak": streak.best_streak
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    tasks = Task.objects.filter(user=request.user)

    data = []
    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "is_completed": task.is_completed
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_streak(request):
    streak, _ = Streak.objects.get_or_create(user=request.user)

    return Response({
        "current_streak": streak.current_streak,
        "best_streak": streak.best_streak,
        "last_completed_date": streak.last_completed_date
    })
