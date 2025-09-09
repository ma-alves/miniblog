from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic

from .models import Post, Author, Comment


def index(request):
    context = {
        "post_list": (post_list := Post.objects.all().order_by("-created_at")),
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
        query = self.request.GET.get("query", "")
        post_list = Post.objects.all().order_by("-created_at")
        if query:
            post_list = post_list.filter(
                Q(content__icontains=query) | Q(title__icontains=query)
            ).order_by("-created_at")
        return post_list


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
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("delete-post", kwargs={"pk": self.object.pk})
            )


@login_required
def like_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, id=pk)
        user = request.user

        if post.user_has_liked(user):
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse(
            {"status": "success", "liked": liked, "count": post.get_like_count()}
        )
    return JsonResponse({"status": "error"}, status=400)


# Não lembro a origem destes comentários (código pré-LLMs)
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
