from django.contrib import admin
from . import models
from ckeditor.widgets import CKEditorWidget


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.RichTextField: {'widget': CKEditorWidget}
    }
    list_display = ('title', 'slug', 'author', 'status', 'publish')


class CatAuth(admin.ModelAdmin):
    list_display = ('title', 'desc')


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc')


class Comments(admin.ModelAdmin):
    list_display = ('post', 'name', 'date_added')

# class ckEditor(admin.ModelAdmin):title


admin.site.register(models.Tags, TagAdmin)
admin.site.register(models.Post, AuthorAdmin)
admin.site.register(models.Category, CatAuth)
admin.site.register(models.Comment, Comments)
