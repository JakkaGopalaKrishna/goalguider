from django.contrib import admin
from .models import Task, Streak

admin.site.register(Task)
admin.site.register(Streak)


# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ("id", "step", "title", "is_completed")
#     list_filter = ("is_completed",)