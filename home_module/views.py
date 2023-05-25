from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views import View
from user_posts.models import UserPost
from django.contrib import messages
from user_posts.forms import PostCreateUpdateForm
# Create your views here.

class HomeView(View):
    def get(self, request):
        post = UserPost.objects.all()
        return render(request, 'home_module/index.html', {'posts':post})

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(UserPost, id=post_id, slug=post_slug)
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
    form_class = PostCreateUpdateForm
    template_name = 'user_posts/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = UserPost.objects.get(id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('home_module:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form':form})

    def post(self, request: HttpRequest, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you post is update', 'success')
            return redirect('home_module:post_detail', post.id, post.slug)

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'user_posts/create.html'

    def get(self, request:HttpRequest, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request:HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'your post create is successfuly', 'success')
            return redirect('home_module:post_detail', new_post.id, new_post.slug)


