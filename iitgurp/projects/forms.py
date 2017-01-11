from __future__ import unicode_literals

from django import forms

from .models import Project, Skill


class ProjectCreateForm(forms.ModelForm):

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
                'class': 'materialize-textarea'
            })
        }
        help_texts = {
            'skills': 'Select at least one tag (for example: Machine Learning)'
        }


class ProjectSearchForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'skills']
        help_texts = {
            'title': 'Title or part of title'
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'materialize-textarea',
            })
        }
