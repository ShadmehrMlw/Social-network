from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from account_module.forms import UserRegistrationForm

# Create your views here.

class RegisterView(View):
    def get(self, request: HttpRequest):
        form = UserRegistrationForm()
        return render(request, 'account_module/register.html', {'form': form})

    def post(self, request: HttpRequest):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'your register is successfuly', 'success')
            return redirect('home_module:home')

