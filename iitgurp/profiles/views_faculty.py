from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, UpdateView

from projects.models import Project, ProjectStudentRelation

from .forms import FacultySearchForm, StudentSearch
from .models import Faculty, Student


class Home(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A view that renders home page of faculty users.
    """
    login_url = reverse_lazy('login')
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
    login_url = reverse_lazy('login')
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
    login_url = reverse_lazy('login')
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


class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    A view that renders detail of Student instance and Projects instances
    related to the Student instance.
    """
    login_url = reverse_lazy('login')
    template_name = 'profiles/faculty/student_detail.html'
    model = Student
    context_object_name = 'stud'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get_context_data(self, **kwargs):
        context = super(StudentDetail, self).get_context_data(**kwargs)
        context['stud_rel_list'] = ProjectStudentRelation.objects.filter(
            student=self.object
        )
        return context


class FacultySearch(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'profiles/faculty/faculty_search.html'
    form_class = FacultySearchForm

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def form_valid(self, form):
        full_name = form.cleaned_data.get('full_name')
        department = form.cleaned_data.get('department')
        if department is not '':
            faculty_list = Faculty.objects.filter(
                full_name__icontains=full_name, department=department
            )
        else:
            faculty_list = Faculty.objects.filter(
                full_name__icontains=full_name)
        args = dict(faculty_list=faculty_list, form=form, results=True)
        return render(self.request, self.template_name, args)


class FacultySearchDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'profiles/faculty/faculty_search_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get(self, request, **kwargs):
        fac = get_object_or_404(Faculty, pk=kwargs.get('pk', None))
        project_list = Project.objects.filter(faculty=fac)
        args = dict(fac=fac, project_list=project_list)
        return render(request, self.template_name, args)


class SearchStudent(LoginRequiredMixin, UserPassesTestMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'profiles/faculty/student_search.html'
    form_class = StudentSearch

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def form_valid(self, form):
        full_name = form.cleaned_data.get('full_name', '')
        stud_list = Student.objects.filter(
            full_name__icontains=full_name
        )
        args = dict(stud_list=stud_list, form=form, results=True)
        return render(self.request, self.template_name, args)


class StudentSearchDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    template_name = 'profiles/faculty/student_search_detail.html'

    def test_func(self):
        return self.request.user.user_type == 'faculty'

    def get(self, request, **kwargs):
        student = get_object_or_404(Student, pk=kwargs.get('pk', None))
        stud_rel_list = ProjectStudentRelation.objects.filter(
            student=student)
        args = dict(stud_rel_list=stud_rel_list, student=student)
        return render(request, self.template_name, args)
