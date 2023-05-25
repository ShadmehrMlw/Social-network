from django import forms
from .models import UserPost

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('body',)
