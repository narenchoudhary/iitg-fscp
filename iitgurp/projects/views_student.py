from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView

from profiles.models import Student

from .models import Project, ProjectStudentRelation


class ProjectList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    model = Project
    template_name = 'projects/student/project_list.html'
    context_object_name = 'project_list'

    def test_func(self):
        return self.request.user.user_type == 'student'


class ProjectDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Project
    template_name = 'projects/student/project_detail.html'
    context_object_name = 'project'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_context_data(self, **kwargs):
        student = get_object_or_404(
            Student, user_profile__username=self.request.user.username)
        try:
            stud_rel = ProjectStudentRelation.objects.get(
                student=student, project=self.object
            )
        except ProjectStudentRelation.DoesNotExist:
            stud_rel = None
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['stud_rel'] = stud_rel
        return context


class ProjectStudRelCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    http_method_names = ['get', 'head', 'options']
    template_name = 'projects/student/project_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request, **kwargs):
        student = get_object_or_404(
            Student, user_profile__username=request.user.username)
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        stud_rel, created = ProjectStudentRelation.objects.get_or_create(
            project=project, student=student
        )
        args = dict(project=project, stud_rel=stud_rel)
        return render(request, self.template_name, args)
