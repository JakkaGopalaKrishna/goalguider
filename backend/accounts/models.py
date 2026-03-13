from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="account_profile"   # 🔥 IMPORTANT
    )
    current_status = models.CharField(max_length=255, blank=True)
    career_goal = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
