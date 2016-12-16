from __future__ import unicode_literals

from django import forms
from django_select2.forms import ModelSelect2MultipleWidget

from .models import Project, Skill


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'description', 'hours_per_week', 'skills',
                  'start_date', 'end_date', 'requirements', 'closing_datetime']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add a title'}),
            'skills': ModelSelect2MultipleWidget(
                queryset=Skill.objects.all().order_by('-name'),
                search_fields=['name', ],
                attrs={'class': 'browser-default'},
            ),
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'closing_datetime': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 97, 'class': 'materialize-textarea'}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'cols': 97, 'class': 'materialize-textarea'})
        }


class ProjectSearchForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'skills']
        widgets = {
            'skills': ModelSelect2MultipleWidget(
                queryset=Skill.objects.all().order_by('-name'),
                search_fields=['name', ],
                attrs={'class': 'browser-default'},
            ),
        }
        help_texts = {
            'title': 'Title or part of title'
        }
