from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy

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
    

class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    permission_required = ['blog.add_post']
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
    

class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title','content']
    permission_required = ['blog.change_post']
    

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
    permission_required = ['blog.delete_post']
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete-post", kwargs={"pk": self.object.pk})
            )
        