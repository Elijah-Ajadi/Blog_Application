from django.utils import timezone
from django import forms
from django.db import models
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password1 and confirm_password and password1 != confirm_password:
            raise ValidationError("Passwords do not match")
        return confirm_password

    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'description',
                  'author', 'image', 'img_desc', 'content', 'category', 'slug',
                  'publish', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            "name": forms.TextInput(attrs=({"placeholder": "Enter your name..."})),
            "comment": forms.Textarea(attrs=({"placeholder": "Enter your comment..."}))
        }
