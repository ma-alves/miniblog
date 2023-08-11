from django.contrib import admin
from .models import Post, PostAuthor, PostComment

# Register your models here.

admin.site.register(PostAuthor)
admin.site.register(PostComment)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_modified')
    ordering = ['date_posted']

admin.site.register(Post, PostAdmin)
