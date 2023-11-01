from typing import Any

from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Post, PostAuthor, User

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
    

class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    permission_required = 'blog.creator'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
    

class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title','content']
    permission_required = 'blog.creator'
    