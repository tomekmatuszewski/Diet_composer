from django.urls import path

from apps.diet_blog import views

urlpatterns = [
    path("blog/", views.blog, name="diet_composer-blog"),
]
