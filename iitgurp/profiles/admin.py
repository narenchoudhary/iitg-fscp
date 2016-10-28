from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, Faculty, Student

admin.site.register(UserProfile)
admin.site.register(Faculty)
admin.site.register(Student)
