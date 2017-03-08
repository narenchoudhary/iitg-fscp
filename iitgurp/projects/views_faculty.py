from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView, View)

from export_csv.views import ExportCSV

from profiles.models import Faculty

from .forms import ProjectCreateForm, ProjectSearchForm, SkillForm
from .models import Project, ProjectStudentRelation, Skill


class ProjectCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View class which handles Project creation
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    object = None
    form_class = ProjectCreateForm
    template_name = 'projects/faculty/project_create.html'

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
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
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('projects:fac-project-detail',
                            args=(self.object.id,))


class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class which handles Project updates
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    model = Project
    form_class = ProjectCreateForm
    template_name = 'projects/faculty/project_update.html'

    def test_func(self):
        """
        Only request by faculty users who created the Project being updated
        should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        is_faculty = self.request.user.user_type == 'faculty'
        if not is_faculty:
            return False
        faculty = get_object_or_404(
            Faculty, user_profile__username=self.request.user.username
        )
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        is_owner = project.faculty == faculty
        if not is_owner:
            return False
        return True

    def get_success_url(self):
        return reverse_lazy('projects:fac-project-detail',
                            args=(self.object.id,))


class ProjectList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View class which renders list of Projects
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    template_name = 'projects/faculty/project_list.html'
    context_object_name = 'project_list'

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'

    def get_queryset(self):
        return Project.objects.filter(
            faculty__user_profile__username=self.request.user.username
        )


class ProjectDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class which renders details of a Project
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    model = Project
    template_name = 'projects/faculty/project_detail.html'
    context_object_name = 'project'

    def test_func(self):
        """
        Only request by faculty users who created the Project being displayed
        should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        is_faculty = self.request.user.user_type == 'faculty'
        if not is_faculty:
            return False
        faculty = get_object_or_404(
            Faculty, user_profile__username=self.request.user.username
        )
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        is_owner = project.faculty == faculty
        if not is_owner:
            return False
        return True

    def get_context_data(self, **kwargs):
        """
        Custom get_context_data method to add student applications to the context.
        :param kwargs: Keyword arguments
        :return: Context
        :rtype: dict
        """
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['stud_rel_list'] = ProjectStudentRelation.objects.filter(
            project=self.object
        ).select_related('student')
        return context


class SearchProject(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    View class which handles searching Projects for faculty users.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    template_name = 'projects/faculty/project_search.html'
    form_class = ProjectSearchForm

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'

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


class ProjectSearchDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class which handles rendering details of Project from search results.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    template_name = 'projects/faculty/project_search_detail.html'
    model = Project
    context_object_name = 'project'

    def test_func(self):
        """
         Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'

    def get_context_data(self, **kwargs):
        context = super(ProjectSearchDetail, self).get_context_data(**kwargs)
        context['stud_rel_list'] = ProjectStudentRelation.objects.filter(
            project=self.object
        )
        return context


class ProjectListCSV(ExportCSV):
    model = Project

    def get_queryset(self):
        return Project.objects.all()


class SkillList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    View class which handles rendering list of Skill instances.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    model = Skill
    template_name = 'projects/faculty/skill_list.html'
    context_object_name = 'skill_list'

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'


class SkillCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View class which handles creating new Skill instances.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    form_class = SkillForm
    template_name = 'projects/faculty/skill_create.html'

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'

    def get_success_url(self):
        return reverse_lazy('projects:fac-skill-detail',
                            args=(self.object.id,))


class SkillDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View class which handles rendering details of a Skill instance.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    model = Skill
    template_name = 'projects/faculty/skill_detail.html'
    context_object_name = 'skill'

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'

    def get_context_data(self, **kwargs):
        context = super(SkillDetail, self).get_context_data(**kwargs)
        skill = Skill.objects.get(id=self.kwargs.get('pk'))
        context['project_list'] = skill.project_set.all()
        return context


class SkillUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class which handles updating an existing Skill instance.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    model = Skill
    form_class = SkillForm
    template_name = 'projects/faculty/skill_update.html'

    def test_func(self):
        """
        Only request by faculty users should be allowed.
        :return: True if test passed otherwise False
        :rtype: bool
        """
        return self.request.user.user_type == 'faculty'

    def get_success_url(self):
        return reverse_lazy('projects:fac-skill-detail',
                            args=(self.object.id,))


class ProjectStudRelUpdate(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View class which handles updating ProjectStudentRelation instances by faculty users.

    Four update operations are possible:
    1. Mark Shortlisted
    2. Undo Shortlisted
    3. Mark Completed
    4. Mark Abandoned

    ``action`` parameter passed in ``url`` us used to run correct update operation.
    """
    login_url = reverse_lazy('login')
    # Instead of raising PermissionDenied exception, redirect to login page.
    raise_exception = False
    template_name = 'projects/faculty/project_detail.html'
    http_method_names = ['get', 'options', 'head']

    def test_func(self):
        """
        Test function to check if logged in user is authorized to proceed. Only
        requests of Faculty users are allowed to execute this View class methods.
        :return:
        """
        return self.request.user.user_type == 'faculty'

    @staticmethod
    def shortlist(rel):
        """
        Mark ProjectStudentRelation instance as shortlisted.
        :param rel: ProjectStudentRelation instance
        :return: None
        """
        if not rel.shortlist_status:
            rel.shortlist_status = True
            rel.shortlist_datetime = timezone.now()
            rel.save()
        return

    @staticmethod
    def undo_shortlist(rel):
        """
        Mark already shortlisted ProjectStudentRelation as not shortlisted.

        If ProjectStudentRelation instance is marked completed or abandoned,
        do not undo shortlist status.

        :param rel: ProjectStudentRelation instance
        :return: None
        """
        if rel.shortlist_status and not rel.completion_status and not rel.abandon_status:
            rel.shortlist_status = False
            rel.shortlist_datetime = None
            rel.save()
        return

    @staticmethod
    def mark_complete(rel):
        """
        Mark already shortlisted ProjectStudentRelation as completed.
        :param rel: ProjectStudentRelation instance
        :return: None
        """
        if rel.shortlist_status and not rel.completion_status:
            rel.completion_status = True
            rel.completion_datetime = timezone.now()
            rel.save()
        return

    @staticmethod
    def mark_abandoned(rel):
        """
        Mark already shortlisted ProjectStudentRelation instance as abandoned.
        :param rel: ProjectStudentRelation instance
        :return: None
        """
        if rel.shortlist_status and not rel.abandon_status:
            rel.abandon_status = True
            rel.abandon_datetime = timezone.now()
            rel.save()
        return

    def get(self, request, relid, action):
        """
        Handle GET request.
        :param request: HttpRequest instance
        :param relid: id of ``ProjectStudentRelation`` instance
        :param action: Integer in [1, 2, 3, 4] used as action identifier.
        :return: HttpResponse instance
        :rtype: HttpResponse
        """
        try:
            rel = ProjectStudentRelation.objects.select_related(
                'project').get(id=relid)
        except ProjectStudentRelation.DoesNotExist:
            raise Http404
        # Cast to integer becuase action is read as character.
        action = int(action)
        if action == 1:
            ProjectStudRelUpdate.shortlist(rel)
        elif action == 2:
            ProjectStudRelUpdate.undo_shortlist(rel)
        elif action == 3:
            ProjectStudRelUpdate.mark_complete(rel)
        elif action == 4:
            ProjectStudRelUpdate.mark_abandoned(rel)
        else:
            # value of action must be in [1, 2, 3, 4].
            # Otherwise, raise 404 error.
            raise Http404
        project = rel.project
        stud_rel_list = ProjectStudentRelation.objects.filter(
            id=project.id).select_related('student')
        context = dict(project=project, stud_rel_list=stud_rel_list)
        return render(request, self.template_name, context)
