from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .constants import LOGIN_SERVER, DEPARTMENT


class LoginForm(forms.Form):
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
    DEPARTMENT_BLANK = DEPARTMENT + [('', '-----')]
    full_name = forms.CharField(max_length=50, required=True,
                                label='Name of Faculty',
                                help_text='Type name or part of name')
    department = forms.ChoiceField(choices=DEPARTMENT_BLANK,
                                   required=False, initial='')


class StudentSearch(forms.Form):
    full_name = forms.CharField(max_length=50, required=True,
                                help_text='Name or part of name')
