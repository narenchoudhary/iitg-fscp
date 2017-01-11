from django.contrib import auth
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic.base import View

from .forms import LoginForm


class LoginView(View):
    """
    A view that handles login functionality
    """
    template_name = 'profiles/login.html'
    port = 995
    next = ''

    def get(self, request):
        self.next = request.GET.get('next', '')
        if request.user.is_authenticated():
            if request.user.user_type == 'admin':
                return None
            elif request.user.user_type == 'faculty':
                return redirect('fac-home')
            elif request.user.user_type == 'student':
                return redirect('stud-home')
        args = dict(form=LoginForm(None), next=self.next)
        return render(request, self.template_name, args)

    def post(self, request):
        redirect_to = request.POST.get('next', self.next)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            server = form.cleaned_data.get('login_server')

            user = auth.authenticate(username=username, password=password,
                                     server=server, port=self.port)
            if user is not None:
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    if user.user_type == 'faculty':
                        auth.login(request=request, user=user)
                        return redirect('fac-home')
                    elif user.user_type == 'student':
                        auth.login(request=request, user=user)
                        return redirect('stud-home')
                    else:
                        form.add_error(None, 'No such user exists.')
                        return render(request, self.template_name,
                                      dict(form=form))
                else:
                    return redirect(redirect_to)
            else:
                form.add_error(None, 'No such user exists.')
                return render(request, self.template_name, dict(form=form))
        else:
            return render(request, self.template_name, dict(form=form))


class LogoutView(View):
    http_method_names = ['get', 'head', 'options']

    def get(self, request):
        auth.logout(request=request)
        return redirect('login')


class HelpPageView(View):
    """
    View that handles help page rendering.
    """
    http_method_names = ['get', 'head', 'options']
    template_name = 'profiles/help.html'

    def get(self, request):
        return render(request, self.template_name)
