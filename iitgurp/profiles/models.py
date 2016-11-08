from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .constants import *


@python_2_unicode_compatible
class UserProfile(AbstractUser):
    """
    UserProfile model class
    """
    user_type = models.CharField(max_length=20, choices=USER_TYPE,
                                 null=False, blank=False)

    def __str__(self):
        return self.username


@python_2_unicode_compatible
class Student(models.Model):
    """
    Student model class
    """
    user_profile = models.OneToOneField(
        UserProfile, null=False, blank=False,
        limit_choices_to={'user_type': 'student'}
    )
    roll_no = models.DecimalField(
        max_digits=10, decimal_places=0, unique=True, null=False, blank=False)
    web_mail = models.EmailField(null=True, blank=False)
    full_name = models.CharField(max_length=100, null=True, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER, null=False,
                              blank=False)
    hostel = models.CharField(max_length=50, choices=HOSTEL, null=False,
                              blank=False)
    room_no = models.CharField(max_length=7, null=True, blank=True)
    mobile_campus = models.CharField(max_length=12, null=True, blank=True)
    alternate_email = models.EmailField(null=True, blank=True)

    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.web_mail

    def save(self, **kwargs):
        self.last_updated = timezone.now()
        super(Student, self).save(**kwargs)


@python_2_unicode_compatible
class Faculty(models.Model):
    """
    Faculty model class
    """
    user_profile = models.OneToOneField(
        UserProfile, null=False, blank=False,
        limit_choices_to={'user_type': 'faculty'}
    )
    web_mail = models.EmailField(null=True, blank=False)
    full_name = models.CharField(max_length=100, null=True, blank=False)
    department = models.CharField(max_length=100, choices=DEPARTMENT,
                                  null=True, blank=True)
    room_no = models.CharField(max_length=7, null=True, blank=True)

    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.web_mail

    def save(self, **kwargs):
        self.last_updated = timezone.now()
        super(Faculty, self).save(**kwargs)
