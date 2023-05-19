from django import forms
from .models import UserPost

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('body',)