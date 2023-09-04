from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Post, PostAuthor

# Create your views here.

def index(request):
    context = {
        'post_list': (post_list := Post.objects.all())
    }
    return render(request, 'index.html', context)


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/posts.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()
    

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'


class AuthorListView(generic.ListView):
    model = PostAuthor
    context_object_name = 'author_list'
    template_name = 'blog/authors.html'
    paginate_by = 10

    def get_queryset(self):
        return PostAuthor.objects.all()


class AuthorDetailView(generic.DetailView):
    model = PostAuthor
    template_name = 'blog/author.html'
    
    
'''
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'
'''