from apps.diet_composer.models.meal import Meal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class DailyMenu(models.Model):

    name = models.CharField(max_length=150)
    number_of_meals = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6), MinValueValidator(1)])
    meals = models.ManyToManyField(Meal, related_name="meals")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_menus")

    def __str__(self):
        return f"Daily Menu {self.name} created by {self.author.username}"



