from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post

# Create your views here.

def index(request):
    return render(request, 'index.html')


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/posts.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()
    