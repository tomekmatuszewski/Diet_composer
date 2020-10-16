from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.diet_blog.models import Comment, Post


class PostListView(ListView):
    model = Post
    template_name = "diet_blog/blog.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    extra_context = {"title": "Blog"}
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = "diet_blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):

    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs.get("pk"))
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blog"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def LikeView(request, pk):

    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post-detail", args=[str(pk)]))
