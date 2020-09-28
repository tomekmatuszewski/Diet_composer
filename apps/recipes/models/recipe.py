from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.users.utils import change_pic_size
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="recipes_pics")
    description = models.TextField()
    preparing_time = models.CharField(help_text="Preparation time in minutes", max_length=10)
    ingredients = models.TextField(help_text="Separate the ingredients on the list "
                                             "with an enter so that they appear one below the other")
    date_public = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    likes = models.ManyToManyField(User, related_name="recipe_post")

    @property
    def total_likes(self):
        return self.likes.count()

    def __repr__(self) -> str:
        return f"{self.title} {self.author}"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        change_pic_size(self.image.path, 300, 300)

    def get_absolute_url(self):
        return reverse("recipe-detail", kwargs={"pk": self.pk})



