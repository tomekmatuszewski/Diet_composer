from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'diet_composer/home.html')


def about(request):
    return render(request, 'diet_composer/about.html', {'title': "About"})
