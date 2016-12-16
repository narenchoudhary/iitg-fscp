from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View, DetailView, FormView, ListView

from profiles.models import Student

from .forms import ProjectSearchForm
from .models import Project, ProjectStudentRelation, Skill


class ProjectList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View which renders list of all Projects when requested by a Student user
    """
    login_url = reverse_lazy('login')
    model = Project
    template_name = 'projects/student/project_list.html'
    context_object_name = 'project_list'

    def test_func(self):
        return self.request.user.user_type == 'student'


class ProjectListBySkill(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'projects/student/skill_detail.html'
    context_object_name = 'project_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        skill = Skill.objects.get(id=self.kwargs.get('pk'))
        return skill.project_set.all()

    def get_context_data(self, **kwargs):
        context = super(ProjectListBySkill, self).get_context_data(**kwargs)
        context['skill'] = Skill.objects.get(id=self.kwargs.get('pk'))
        return context


class ProjectDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View that renders details of Project instance when requested by a Student
    user
    """
    login_url = reverse_lazy('login')
    model = Project
    template_name = 'projects/student/project_detail.html'
    context_object_name = 'project'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_context_data(self, **kwargs):
        student = get_object_or_404(
            Student, user_profile__username=self.request.user.username)
        # get the relation instance if it exists.
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
        # get_or_create returns a tuple but since tuple returned if of no use
        # here no variable has been assigned the return value.
        # create a ProjectStudentRelation instance if it does not exist
        # already.
        ProjectStudentRelation.objects.get_or_create(
            project=project, student=student
        )
        return redirect('projects:stud-project-detail', pk=project.id)


class ProjectStudRelDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    http_method_names = ['get', 'head', 'options']
    template_name = 'projects/student/project_detail.html'
    project = None
    student = None

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get(self, request, **kwargs):
        student = get_object_or_404(
            Student, user_profile__username=request.user.username)
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        # student can remove application only before closing deadline
        if project.closing_datetime >= timezone.now():
            ProjectStudentRelation.objects.filter(
                project=project, student=student
            ).delete()
            return redirect('projects:stud-project-detail', pk=project.id)
        else:
            return HttpResponseForbidden()


class SearchProject(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'projects/student/project_search.html'
    form_class = ProjectSearchForm

    def test_func(self):
        return self.request.user.user_type == 'student'

    def form_valid(self, form):
        title = form.cleaned_data.get('title', '')
        skills = form.cleaned_data.get('skills', [])
        if skills:
            project_list = Project.objects.filter(
                title__icontains=title, skills__in=skills
            )
        else:
            project_list = Project.objects.filter(
                title__icontains=title
            )
        args = dict(project_list=project_list, form=form, results=True)
        return render(self.request, self.template_name, args)


class ProjectStudentRelationList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'projects/student/project_stud_rel_list.html'
    context_object_name = 'project_rel_list'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_queryset(self):
        return ProjectStudentRelation.objects.filter(
            student__user_profile=self.request.user
        )
