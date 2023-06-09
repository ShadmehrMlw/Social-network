from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account_module.forms import UserRegistrationForm, UserLoginForm
from user_posts.models import UserPost
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy

# Create your views here.

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account_module/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_module:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            messages.success(request, 'your register is successfuly', 'success')
            return redirect('home_module:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account_module/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_module:home')
        return super().dispatch(request, *args, **kwargs)
    
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


class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request, 'your logout is successfuly!', 'success')
        return redirect('home_module:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account_module/profile.html'
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        post = get_list_or_404(UserPost, id=user_id)
        context = {
            'user': user,
            'posts': post,
        }
        return render(request, self.template_name, context)


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'account_module/password_reset_form.html'
    success_url = reverse_lazy('account_module:password_reset_done')
    email_template_name = 'account_module/password_email_reset.html'


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'account_module/password_reset_done.html'