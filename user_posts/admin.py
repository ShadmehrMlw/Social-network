from django.contrib import admin
from .models import UserPost
# Register your models here.

@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'slug', 'created', 'update']
    search_fields = ['slug']
    list_filter = ['update']
    prepopulated_fields = {'slug':('body',)}
    raw_id_fields = ('user',)