from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="diet_composer-home"),
    path("about/", views.about, name="diet_composer-about"),
]
