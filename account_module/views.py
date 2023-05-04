from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from account_module.forms import UserRegistrationForm

# Create your views here.

class RegisterView(View):
    def get(self, request:HttpRequest):
        form = UserRegistrationForm()
        return render(request, 'account_module/register.html', {'form': form})


