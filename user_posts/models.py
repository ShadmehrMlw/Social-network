from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('home_module:post_detail', args=(self.id, self.slug))

