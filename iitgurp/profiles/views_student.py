from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, UpdateView

from .models import Student


class Home(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A view that redirects to home page of student users.
    """
    template_name = 'profiles/student/home.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request):
        stud = get_object_or_404(
            Student, user_profile__username=request.user.username)
        return render(request, self.template_name, dict(stud=stud))


class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders details of instance of Student model
    """
    template_name = 'profiles/student/student_detail.html'
    model = Student
    context_object_name = 'stud'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student, user_profile__username=self.request.user.username
        )


class StudentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A view that updates instance of Student model.
    """
    template_name = 'profiles/student/student_update.html'
    model = Student
    fields = ['hostel', 'room_no', 'mobile_campus', 'alternate_email']

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student, user_profile__username=self.request.user.username
        )

    def get_success_url(self):
        return reverse_lazy('stud-detail')
