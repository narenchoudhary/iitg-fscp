from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, UpdateView

from projects.models import Project

from .forms import FacultySearchForm, StudentUpdateForm
from .models import Faculty, Student


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
    login_url = reverse_lazy('login')
    template_name = 'profiles/student/student_update.html'
    form_class = StudentUpdateForm

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student, user_profile__username=self.request.user.username
        )

    def get_success_url(self):
        return reverse_lazy('stud-detail')

    def get_form(self, form_class=None):
        form = super(StudentUpdate, self).get_form(form_class)
        # form.fields['hostel'].widget.attrs['class'] = 'browser-default'
        return form


class FacultySearch(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    View that handles searching Faculty instances on student side.
    """
    login_url = reverse_lazy('login')
    template_name = 'profiles/student/faculty_search.html'
    form_class = FacultySearchForm

    def test_func(self):
        return self.request.user.user_type == 'student'

    def form_valid(self, form):
        full_name = form.cleaned_data.get('full_name', None)
        department = form.cleaned_data.get('department', '')
        if department != '':
            fac_list = Faculty.objects.filter(
                full_name__icontains=full_name, department=department
            )
        else:
            fac_list = Faculty.objects.filter(full_name__icontains=full_name)
        args = dict(fac_list=fac_list, form=form, results=True)
        return render(self.request, self.template_name, args)


class FacultyDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View that renders Faculty instance details when requested by a Student
    user.
    """
    login_url = reverse_lazy('login')
    template_name = 'profiles/student/faculty_detail.html'
    model = Faculty
    context_object_name = 'fac'

    def test_func(self):
        return self.request.user.user_type == 'student'

    def get_context_data(self, **kwargs):
        context = super(FacultyDetail, self).get_context_data(**kwargs)
        context['project_list'] = Project.objects.filter(faculty=self.object)
        return context
