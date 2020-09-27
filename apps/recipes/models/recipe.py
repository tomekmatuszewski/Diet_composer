from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.users.utils import change_pic_size


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default="default.jpg", upload_to="recipes_pics")
    content = models.TextField()
    date_public = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # ingredients = models.JSONField()

    # likes = models.ManyToManyField(User, related_name="blog_post")

    def __repr__(self) -> str:
        return f"{self.title} {self.author}"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        change_pic_size(self.image.path, 500, 500)
