from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _

from .models import Project, Skill


class ProjectCreateForm(forms.ModelForm):
    """
    ModelForm for creating and updating a Project.
    """

    class Meta:
        model = Project
        fields = ['title', 'description', 'hours_per_week', 'start_date',
                  'end_date', 'requirements', 'closing_datetime', 'skills']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'closing_datetime': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea',
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'materialize-textarea',
                'placeholder': _('Example: CPI must be greater than 5. No active backlogs.')
            })
        }
        help_texts = {
            'skills': _('Select at least one tag (for example: Machine Learning)')
        }


class ProjectSearchForm(forms.ModelForm):
    """
    ModelForm for searching a Project.
    """

    class Meta:
        model = Project
        fields = ['title', 'skills']
        labels = {
            'title': _('Title or part of title')
        }


class SkillForm(forms.ModelForm):
    """
    ModelForm for creating and updating a Skill.
    """

    class Meta:
        model = Skill
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea',
            })
        }
