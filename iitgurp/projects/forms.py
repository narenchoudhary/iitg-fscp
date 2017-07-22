from __future__ import unicode_literals

from django import forms
from django.utils import timezone
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

    def clean(self):
        super(ProjectCreateForm, self).clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        closing_datetime = self.cleaned_data.get("closing_datetime")
            
        closing_date = closing_datetime.date()
        if timezone.now() >= closing_datetime:
            self.add_error(
                'closing_datetime',
                _('Closing Datetime must be a date in future.')
            )
        if closing_date >= start_date:
            self.add_error(
                'closing_datetime', 
                _("Closing Datetime must be smaller than Tentative Start Date.")    
            )
        if start_date >= end_date:
            self.add_error(
                'start_date', 
                _("Tentative Start Date must be smaller than Tentative End Date.")
            )


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
