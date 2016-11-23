from __future__ import unicode_literals

from django import forms

from bootstrap3_datetime.widgets import DateTimePicker
from django_select2.forms import ModelSelect2MultipleWidget

from .models import Project, Skill


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'description', 'hours_per_week', 'skills',
                  'start_date', 'end_date', 'requirements', 'closing_datetime']
        widgets = {
            'skills': ModelSelect2MultipleWidget(
                queryset=Skill.objects.all().order_by('-name'),
                search_fields=['name', ]
            ),
            'start_date': DateTimePicker(options={
                "format": "YYYY-MM-DD", "pickTime": False
            }),
            'end_date': DateTimePicker(options={
                "format": "YYYY-MM-DD", "pickTime": False
            }),
            'closing_datetime': DateTimePicker(options={
                "format": "YYYY-MM-DD HH:mm", "pickTime": True
            }),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 97}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'cols': 97})
        }


class ProjectSearchForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'skills']
        widgets = {
            'skills': ModelSelect2MultipleWidget(
                queryset=Skill.objects.all().order_by('-name'),
                search_fields=['name', ]
            ),
        }
        help_texts = {
            'title': 'Title or part of title'
        }
