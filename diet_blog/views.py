from django.shortcuts import render
from diet_blog.models import *


def blog(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'diet_blog/blog.html', context)
