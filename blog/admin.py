from django.contrib import admin
from .models import Post, PostAuthor, PostComment

# Register your models here.

admin.site.register(PostAuthor)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_modified')
    ordering = ['date_posted']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('content_limit', 'main_post', 'comment_author', 'date_posted', 'last_modified')
    ordering = ['date_posted']

    @admin.display(description="Content")
    def content_limit(self, obj):
        return f'{obj.content}'[:15] + '...'
