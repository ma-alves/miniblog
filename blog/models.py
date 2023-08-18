from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class PostAuthor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    bio = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=2000)
    likes = models.IntegerField(default=0)

    author = models.ForeignKey(
        PostAuthor,
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )
    
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    content = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    comment_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )

    main_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )

    def __str__(self) -> str:
        return self.content[:15] + "..."
    