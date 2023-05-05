from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from account_module.forms import UserRegistrationForm

# Create your views here.

class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account_module/register.html'
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

