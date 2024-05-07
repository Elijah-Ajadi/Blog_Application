from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

from django.core.exceptions import ValidationError


# Create your models here.


class Category(models.Model):
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created_at")
    # updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated_at")
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=500)

    #
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title




class Post(models.Model):
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='pics/', null=True, blank=True)
    img_desc = models.CharField(max_length=300)
    publish = models.DateTimeField(default=timezone.now)
    content = RichTextField()
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=options, default='draft')

    # newmanager = NewManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True, null=True)
    email = models.EmailField(max_length=254)
    bio = models.CharField(null=True, max_length=500)
    phone_number = models.CharField(max_length=15)
