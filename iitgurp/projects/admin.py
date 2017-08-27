from django.contrib import admin

from .models import Project, ProjectStudentRelation, Skill

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(ProjectStudentRelation)
