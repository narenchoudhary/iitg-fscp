from __future__ import unicode_literals

import csv

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponse
from django.utils.encoding import force_str, force_text
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, FormView

from .forms import BooleanFieldBaseForm


class ExportCSV(View):
    """
    View class which handles exporting queryset to CSV file and rendering the
    response.

    :model is an optional name of a model. If provided, all objects of the
    model will for the queryset. If omitted, :get_queryset method must be
    overridden.

    :fields is an optional list of field names which are retrieved from
    queryset and written to CSV. If provided, only the named fields will be
    included in the CSV. If omitted all fields of the model will be used.
    Fields will be written in the CSV in the order of their occurrence in list.

    :filename is an optional string which forms name of csv returned in the
    response. If omitted, 'model_list.csv' will be used.

    :header_row is an optional list of strings which forms the header row of
    the CSV. If omitted, CSV will be created without any header row.

    :content_type is the content_type header of the response. Default value is
    'text/csv' and should not be overridden.
    """

    http_method_names = ['options', 'head', 'get']
    model = None
    fields = []
    filename = None
    header_row = []
    _content_type = 'text/csv'

    def get_queryset(self):
        if self.model is not None:
            queryset = self.model.objects.all()
        else:
            raise ImproperlyConfigured(
                _("No model to get queryset from. Either provide a model or "
                    "override get_queryset method.")
            )
        return queryset

    def get_fields(self):
        if self.fields:
            return self.fields
        if self.model is not None:
            fields = self.model._meta.fields
            for field in fields:
                self.fields.append(field.name)
        else:
            raise ImproperlyConfigured(
                _("No model to get fields form. Either provide a model or "
                  "override get_fields method.")
            )
        return self.fields

    def get_filename(self):
        if self.filename is not None:
            return self.filename
        if self.model is not None:
            self.filename = force_str(self.model.__name__ + '_list.csv')
        else:
            raise ImproperlyConfigured(
                _("No model to generate filename. Either provide model or "
                  "filename or override get_filename method.")
            )
        return self.filename

    def get_header_row(self):
        return self.header_row

    def _create_csv(self):
        response = HttpResponse(content_type=self._content_type)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            self.get_filename())
        wr = csv.writer(response)
        if self.header_row:
            wr.writerow(self.get_header_row())
        queryset = self.get_queryset()
        fields = self.get_fields()
        if queryset is not None:
            for obj in queryset:
                row = []
                for field in iter(fields):
                    value = getattr(obj, field)
                    if hasattr(self, 'clean_%s' % field):
                        clean_func = getattr(self, 'clean_%s' % field)
                        value = clean_func(value)
                    else:
                        value = force_text(value)
                    row.append(value)
                wr.writerow(row)
        return response

    def get(self, request):
        return self._create_csv()


class ExportCSVForm(FormView):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head',
                         'options', 'trace']
    form_class = None
    model = None
    fields = []
    exclude = []
    template_name = None
    filename = None
    header_row = []
    _content_type = 'text/csv'

    def get_form(self, form_class=None):
        if self.form_class is not None:
            if isinstance(self.form_class, forms.Form):
                return self.form_class
            else:
                raise ImproperlyConfigured(
                    _("form_class must be an instance of forms.Form.")
                )
        elif self.model is not None:
            if isinstance(self.model, models.Model):
                self.form_class = self._get_boolean_field_form()
                return self.form_class
            else:
                raise ImproperlyConfigured(
                    _("model must be an instance of models.Model.")
                )
        else:
            raise ImproperlyConfigured(
                _("Both form_class and model cannot be None.")
            )

    def _get_boolean_field_form(self):
        self.form_class = BooleanFieldBaseForm(
            model=self.model, fields=self.fields, exclude=self.exclude)
        return self.form_class

    def get_queryset(self):
        if self.model is not None:
            queryset = self.model.objects.all()
        else:
            raise ImproperlyConfigured(
                _("No model to get queryset from. Either provide a model or "
                    "override get_queryset method.")
            )
        return queryset

    def get_filename(self):
        if self.filename is not None:
            return self.filename
        if self.model is not None:
            self.filename = force_str(self.model.__name__ + '_list.csv')
        else:
            raise ImproperlyConfigured(
                _("No model to generate filename. Either provide model or "
                  "filename or override get_filename method.")
            )
        return self.filename

    def get_field_names(self):
        if self.model is not None:
            if self.fields:
                return self.fields
            elif self.exclude:
                model_fields = [f.name for f in self.model._meta.get_fields()]
                self.fields = [f for f in model_fields if f not in
                               self.exclude]
                return self.fields
        form_fields = self.form_class.fields.items()
        field_names = [k for k, v in form_fields]
        return field_names

    def get_header_row(self):
        return self.header_row

    def _create_csv(self):
        response = HttpResponse(content_type=self._content_type)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            self.get_filename())
        wr = csv.writer(response)
        if self.header_row:
            wr.writerow(self.get_header_row())
        queryset = self.get_queryset()
        fields = self.get_field_names()
        if queryset is not None:
            for obj in queryset:
                row = []
                for field in iter(fields):
                    value = getattr(obj, field)
                    if hasattr(self, 'clean_%s' % field):
                        clean_func = getattr(self, 'clean_%s' % field)
                        value = clean_func(value)
                    else:
                        value = force_text(value)
                    row.append(value)
                wr.writerow(row)
        return response

    def form_valid(self, form):
        return self._create_csv()
