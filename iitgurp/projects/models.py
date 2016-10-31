from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import smart_str, python_2_unicode_compatible
from django.utils import timezone


from profiles.models import Faculty, Student


@python_2_unicode_compatible
class Skill(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    area = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Project(models.Model):
    faculty = models.ForeignKey(Faculty, null=True, blank=False)
    title = models.CharField(max_length=70, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    hours_per_week = models.DecimalField(
        max_digits=3, decimal_places=1, null=False, blank=False, default=2,
        verbose_name='Hours Per Week'
    )
    skills = models.ManyToManyField(Skill, blank=True)
    # dates
    creation_datetime = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)
    # deletion status
    is_deleted = models.BooleanField(default=False, blank=True)
    deletion_datetime = models.DateTimeField(null=True, blank=True)

    @property
    def skill_count(self):
        return self.skills.count()

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        self.last_updated = timezone.now()
        super(Project, self).save(**kwargs)


@python_2_unicode_compatible
class ProjectStudentRelation(models.Model):
    project = models.ForeignKey(Project, null=False, blank=False)
    student = models.ForeignKey(Student, null=False, blank=False)
    creation_datetime = models.DateTimeField(null=False, blank=False)

    class Meta:
        unique_together = ['project', 'student']

    def __str__(self):
        return smart_str(self.project) + smart_str(self.student)

    def save(self, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        super(ProjectStudentRelation, self).save(**kwargs)
