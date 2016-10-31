from __future__ import unicode_literals

from django import forms

from django_select2.forms import ModelSelect2MultipleWidget

from .models import Project, Skill


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'description', 'hours_per_week', 'skills']
        widgets = {
            'skills': ModelSelect2MultipleWidget(
                queryset=Skill.objects.all().order_by('-name'),
                search_fields=['name', ]
            )
        }
