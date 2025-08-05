from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic

from .models import Post, Author, Comment


def index(request):
    context = {
        "post_list": (post_list := Post.objects.all().order_by("-date_posted")),
        "author_list": (author_list := Author.objects.all().order_by("user")),
    }
    return render(request, "index.html", context)


class AuthorListView(generic.ListView):
    model = Author
    template_name = "blog/authors.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        author_list = Author.objects.all()
        if query:
            author_list = author_list.filter(user__username__icontains=query)
            print('bateu')
        return author_list


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "blog/author.html"


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ["bio"]
    permission_required = ["blog.creator"]


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/posts.html"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by("-date_posted")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"


class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    permission_required = ["blog.creator"]

    def form_valid(self, form):
        """Referencia o autor do post à fk do post."""
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    permission_required = ["blog.creator"]


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts")
    permission_required = ["blog.creator"]

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)  # type: ignore
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete-post", kwargs={"pk": self.object.pk})  # type: ignore
            )


class CommentCreate(PermissionRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]
    permission_required = ["blog.creator"]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the post from id and add it to the context
        context["main_post"] = get_object_or_404(Post, pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        # Add logged-in user as author of comment
        form.instance.comment_author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.main_post = get_object_or_404(Post, pk=self.kwargs["pk"])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "post",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
