from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_str, python_2_unicode_compatible
from django.utils.translation import ugettext as _


from profiles.models import Faculty, Student

date_input_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y']
datetime_input_formats = ['%Y-%m-%d %H:%M']


@python_2_unicode_compatible
class Skill(models.Model):
    name = models.CharField(unique=True, max_length=40, null=False, blank=False, help_text=_("Example: Machine Learning"))
    description = models.CharField(
            max_length=600, null=True, blank=False, 
            help_text=_("Example: Machine learning revolves around developing "
            "self-learning computer algorithms that function by virtue of "
            "discovering patterns in data and making intelligent decisions "
            "based on such patterns."))
    created_on = models.DateTimeField(null=False, blank=True)
    last_updated_on = models.DateTimeField(null=False, blank=True)

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        self.last_updated_on = timezone.now()
        super(Skill, self).save(**kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        get_latest_by = 'last_updated_on'


@python_2_unicode_compatible
class Project(models.Model):
    faculty = models.ForeignKey(Faculty, null=True, blank=False)
    title = models.CharField(max_length=70, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    hours_per_week = models.DecimalField(
        max_digits=3, decimal_places=1, null=False, blank=False, default=2,
        verbose_name='Hours Per Week'
    )
    # duration
    start_date = models.DateField(null=True, blank=False,
                                  verbose_name='Tentative Start Date')
    end_date = models.DateField(null=True, blank=False,
                                verbose_name='Tentative End Date')
    # skills/prerequisites
    skills = models.ManyToManyField(Skill, blank=True, verbose_name='Tags')
    requirements = models.TextField(null=True, blank=True, max_length=400,
                                    verbose_name='Other Requirements')
    # dates
    creation_datetime = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)
    closing_datetime = models.DateTimeField(
        null=True, blank=True, verbose_name='Closing Date',
        help_text='Applications will close after this date.'
    )
    # deletion status
    is_deleted = models.BooleanField(default=False, blank=True)
    deletion_datetime = models.DateTimeField(null=True, blank=True)
    # applicants
    applicants = models.ManyToManyField(
        Student, through='ProjectStudentRelation')

    @property
    def is_closed(self):
        return self.closing_datetime < timezone.now()

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

    class Meta:
        ordering = ['-closing_datetime']


@python_2_unicode_compatible
class ProjectStudentRelation(models.Model):
    project = models.ForeignKey(Project, null=False, blank=False,
                                on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=False, blank=False,
                                on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(null=False, blank=False)
    last_updated = models.DateTimeField(null=True, blank=True)
    # shortlist status
    shortlist_status = models.NullBooleanField(default=None, blank=False)
    shortlist_datetime = models.DateTimeField(null=True, blank=True)
    # completion status
    completion_status = models.NullBooleanField(default=None, blank=False)
    completion_datetime = models.DateTimeField(null=True, blank=True)
    # abandon status
    abandon_status = models.NullBooleanField(default=None, blank=False)
    abandon_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['last_updated']
        unique_together = ['project', 'student']

    def __str__(self):
        return smart_str(self.project) + smart_str(self.student)

    @property
    def status(self):
        if self.completion_status:
            return 'Completed'
        elif self.shortlist_status:
            return 'Shortlisted/Ongoing'
        else:
            return '---'

    def save(self, **kwargs):
        if not self.id:
            self.creation_datetime = timezone.now()
        self.last_updated = timezone.now()
        super(ProjectStudentRelation, self).save(**kwargs)
