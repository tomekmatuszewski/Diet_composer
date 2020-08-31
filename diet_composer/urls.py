from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='diet-composer-home'),
    path('about/', views.about, name='diet-composer-about'),
]
