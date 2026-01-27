# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from .models import Roadmap, RoadmapStep, Task

# admin.site.register(Roadmap)
# admin.site.register(RoadmapStep)
# admin.site.register(Task)

from django.contrib import admin
from .models import Roadmap, RoadmapStep


class RoadmapStepInline(admin.TabularInline):
    model = RoadmapStep
    extra = 0


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("user__username",)
    inlines = [RoadmapStepInline]


@admin.register(RoadmapStep)
class RoadmapStepAdmin(admin.ModelAdmin):
    list_display = ("id", "roadmap", "title")
    list_filter = ("roadmap",)


