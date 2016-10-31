from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from profiles.models import Faculty

from .forms import ProjectCreateForm
from .models import Project, ProjectStudentRelation


class ProjectCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View class which handles Project creation
    """
    login_url = reverse_lazy('login')
    object = None
    form_class = ProjectCreateForm
    template_name = 'projects/faculty/project_create.html'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def form_valid(self, form):
        faculty_username = self.request.user.username
        try:
            faculty = Faculty.objects.get(
                user_profile__username=faculty_username)
        except Faculty.DoesNotExist:
            faculty = None

        self.object = form.save()
        self.object.faculty = faculty
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('projects:fac-project-detail',
                            args=(self.object.id,))


class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class which handles Project updates
    """
    login_url = reverse_lazy('login')
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/faculty/project_update.html'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get_success_url(self):
        return reverse_lazy('projects:fac-project-detail',
                            args=(self.object.id,))


class ProjectList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View class which renders list of Projects
    """
    login_url = reverse_lazy('login')
    template_name = 'projects/faculty/project_list.html'
    context_object_name = 'project_list'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get_queryset(self):
        return Project.objects.filter(
            faculty__user_profile__username=self.request.user.username
        )


class ProjectDetail(DetailView):
    """
    View class which renders details of a Project
    """
    model = Project
    template_name = 'projects/faculty/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['stud_rel_list'] = ProjectStudentRelation.objects.filter(
            project=self.object
        )
        return context
