from pyexpat.errors import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, RedirectView

import setting.settings as setting
# from login.form import RegisterForm


class LoginFormView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
       if request.user.is_authenticated:
           return HttpResponseRedirect(setting.LOGIN_REDIRECT_URL)
       return super().dispatch(request,*args, **kwargs)



class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class RegisterView(View):
    def get(self, request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'login.html', data)

    def post(self, request):
        user_created = RegisterForm(data=request.POST)
        if user_created.is_valid():
            user = user_created.save()
            user = authenticate(username=user_created.cleaned_data['username'],
                                password=user_created.cleaned_data['password1'])
            login(request, user)
            return redirect(setting.LOGIN_REDIRECT_URL)

        data = {
            'form': user_created
        }
        return render(request, 'login.html', data)
