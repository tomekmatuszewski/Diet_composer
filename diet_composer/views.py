from django.shortcuts import render

# Create your views here.

user = [
    {'username': "tm050288",
     'email': "tm@gmail.com",
     'password': "12345",
     'reg_date': "12345"},
]


def home(request):
    return render(request, 'diet_composer/home.html')


def about(request):
    return render(request, 'diet_composer/about.html')
