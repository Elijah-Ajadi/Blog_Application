from django.utils import timezone
from django import forms
from django.db import models
from .models import Post, Comment
from ckeditor.fields import RichTextField


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
