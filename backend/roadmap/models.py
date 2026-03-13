from django.db import models
from django.contrib.auth.models import User

class Roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal}"

class RoadmapStep(models.Model):
    roadmap = models.ForeignKey(
        Roadmap,
        on_delete=models.CASCADE,
        related_name="steps"
    )
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"
