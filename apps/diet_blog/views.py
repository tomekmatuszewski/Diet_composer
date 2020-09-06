from django.shortcuts import render

from apps.diet_blog.models import Post


def blog(request):
    context = {"posts": Post.objects.all()}
    return render(request, "diet_blog/blog.html", context)
