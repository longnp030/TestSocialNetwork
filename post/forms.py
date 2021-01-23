from django import forms

from .models import *

class PostCreationForm(forms.ModelForm):
    text = forms.CharField(
        max_length=1000, required=False,
        widget=forms.TextInput,
    )
    images = forms.ModelChoiceField(
        queryset=PostImage.objects.all(),
        required=False,
    )

    class Meta:
        model = Post
        fields = ['text', 'images', ]