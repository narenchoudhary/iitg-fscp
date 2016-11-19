from __future__ import unicode_literals

from django import forms
from django.forms import fields_for_model


class BooleanFieldBaseForm(forms.Form):

    def __init__(self, model=None, fields=None, exclude=None, **kwargs):
        super(BooleanFieldBaseForm, self).__init__(**kwargs)

        model_fields = fields_for_model(model=model, fields=fields,
                                        exclude=exclude)

        for k, v in iter(model_fields.items()):
            form_field = forms.BooleanField()
            form_field.widget = forms.CheckboxInput()
            form_field.label = k
            form_field.required = False
            self.fields.append(form_field)
