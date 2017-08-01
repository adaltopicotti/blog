from django.contrib import admin
from .models import Post, Comment, ForLogic
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ForLogic)
