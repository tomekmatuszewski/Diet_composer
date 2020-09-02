from django.shortcuts import render
from diet_composer.models import *


def home(request):
    return render(request, 'diet_composer/home.html')


def about(request):
    return render(request, 'diet_composer/about.html', {'title': "About"})


def blog(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'diet_composer/blog.html', context)
