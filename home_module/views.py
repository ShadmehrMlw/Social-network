from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from user_posts.models import UserPost
from django.contrib import messages
from user_posts.forms import PostUpdateForm
# Create your views here.

class HomeView(View):
    def get(self, request):
        post = UserPost.objects.all()
        return render(request, 'home_module/index.html', {'posts':post})

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = UserPost.objects.get(id=post_id, slug=post_slug)
        return render(request, 'home_module/detail.html', {'posts':post})

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = UserPost.objects.get(id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted is successfuly', 'success')
        else:
            messages.error(request, 'ypu cant delete this post', 'danger')
        return redirect('home_module:home')

class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'user_posts/update.html'

    def dispatch(self, request, *args, **kwargs):
        post = UserPost.objects.get(id=kwargs['post_id'])
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('home_module:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, post_id):
        post = UserPost.objects.get(id=post_id)
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form':form})

    def post(self, request: HttpRequest, post_id):
        pass

