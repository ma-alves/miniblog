from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Post, Author, Comment

# Register your models here.


class AuthorInline(admin.StackedInline):
    model = Author


class UserAdmin(BaseUserAdmin):
    '''Extends the UserAdmin'''
    inlines = (AuthorInline,)
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Author)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_modified')
    ordering = ['date_posted']


@admin.register(Comment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('content_limit', 'main_post', 'comment_author', 'date_posted', 'last_modified')
    ordering = ['date_posted']

    @admin.display(description="Content")
    def content_limit(self, obj):
        return f'{obj.content}'[:15] + '...'
