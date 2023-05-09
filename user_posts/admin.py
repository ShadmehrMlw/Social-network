from django.contrib import admin
from .models import UserPost
# Register your models here.

class UserPostAdmin(admin.ModelAdmin):
    list_display = ['slug', 'user', 'created', 'update']


admin.site.register(UserPost, UserPostAdmin)
