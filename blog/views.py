from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Post, PostAuthor, PostComment


def index(request):
    context = {
        'post_list': (post_list := Post.objects.all())
    }
    return render(request, 'index.html', context)


class PostListView(generic.ListView):
    model = Post
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
    

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = PostAuthor
    fields = ['bio']
    permission_required = ['blog.change_']

class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    permission_required = ['blog.creator']
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
    

class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title','content']
    permission_required = ['blog.creator']
    

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
    permission_required = ['blog.creator']
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete-post", kwargs={"pk": self.object.pk})
            )
    

class CommentCreate(PermissionRequiredMixin, CreateView):
    model = PostComment
    fields = ['content']
    permission_required = ['blog.creator']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the post from id and add it to the context
        context['main_post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        #Add logged-in user as author of comment
        form.instance.comment_author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.main_post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('post', kwargs={'pk':self.kwargs['pk'],})
