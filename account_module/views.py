from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from account_module.forms import UserRegistrationForm, UserLoginForm


# Create your views here.

class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account_module/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_module:home')
        return super().dispatch(self, request, *args, **kwargs)

    def get(self, request: HttpRequest):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'your register is successfuly', 'success')
            return redirect('home_module:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'account_module/login.html'
    def get(self, request: HttpRequest):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'your loggin is successfuly!', 'success')
                return redirect('home_module:home')
            messages.error(request, 'your username or password is wrong...', 'warning')
        return render(request, self.template_name, {'form':form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'your logout is successfuly!', 'success')
        return redirect('home_module:home')