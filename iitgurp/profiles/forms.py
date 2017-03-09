from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .constants import LOGIN_SERVER, DEPARTMENT
from .models import Student


class LoginForm(forms.Form):
    """
    Login Form
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    login_server = forms.ChoiceField(required=True, choices=LOGIN_SERVER)

    def clean_login_server(self):
        valid_servers = ['202.141.80.9', '202.141.80.10', '202.141.80.11',
                         '202.141.80.12', '202.141.80.13']
        login_server = self.cleaned_data.get('login_server')
        if login_server not in valid_servers:
            raise ValidationError(_('Invalid Login Server'), code='invalid')
        return login_server


class FacultySearchForm(forms.Form):
    """
    Form for searching Faculty instances.
    """
    DEPARTMENT_BLANK = DEPARTMENT + [('', '-----')]
    full_name = forms.CharField(max_length=50, required=True,
                                label=_('Full name or part of name'))
    department = forms.ChoiceField(choices=DEPARTMENT_BLANK,
                                   required=False, initial='',
                                   widget=forms.Select()
                                   )


class StudentSearch(forms.Form):
    """
    For for searching Student instances.
    """
    full_name = forms.CharField(max_length=50, required=True,
                                label=_('Full name or part of name'))


class StudentUpdateForm(forms.ModelForm):
    """
    Form for updating Student instances.
    """
    class Meta:
        model = Student
        fields = ['bio', 'hostel', 'room_no', 'mobile_campus',
                  'alternate_email', 'year_of_admission', 'department',
                  'discipline', 'programme']
        widgets = {'bio': forms.Textarea(attrs={
            'class': 'materialize-textarea'
        })}
