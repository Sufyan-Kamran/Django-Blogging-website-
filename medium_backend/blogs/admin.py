from django.contrib import admin

from .models import Comment, Like, Post, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
