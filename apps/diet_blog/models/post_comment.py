from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.diet_blog.models import Post


class Comment(models.Model):

    content = models.TextField()
    date_comment = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.content}"
