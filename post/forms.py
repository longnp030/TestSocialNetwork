from django import forms

from .models import *

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', ]

class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(
        max_length=100, required=True,
        widget=forms.FileInput
    )
    
    class Meta:
        model = Image
        fields = ['image', ]
    
class PostAddImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['images', ]

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['receiver', 'text', 'images', ]