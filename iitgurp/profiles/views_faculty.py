from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, DetailView

from .models import Faculty


class Home(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A view that renders home page of faculty users.
    """
    template_name = 'profiles/faculty/home.html'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get(self, request):
        faculty = get_object_or_404(
            Faculty, user_profile__username=request.user.username)
        return render(request, self.template_name, dict(fac=faculty))


class FacultyDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders details of instance of Faculty model
    """
    template_name = 'profiles/faculty/faculty_detail.html'
    model = Faculty
    context_object_name = 'fac'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Faculty, user_profile__username=self.request.user.username
        )


class FacultyUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view that updates instance of Faculty model.
    """
    template_name = 'profiles/faculty/faculty_update.html'
    model = Faculty
    fields = ['web_mail', 'department', 'room_no']
    success_url = reverse_lazy('fac-detail')

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Faculty, user_profile__username=self.request.user.username
        )
