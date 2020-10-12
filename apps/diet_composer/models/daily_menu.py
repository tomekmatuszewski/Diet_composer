from apps.diet_composer.models.meal import Meal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class DailyMenu(models.Model):

    name = models.CharField(max_length=150)
    number_of_meals = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6), MinValueValidator(1)])
    meals = models.ManyToManyField(Meal, related_name="menus", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_menus")

    def __str__(self):
        return f"Daily Menu {self.name} created by {self.author.username}"

    @property
    def get_meals_number(self):
        return range(1, self.number_of_meals+1)

    @property
    def total_calories(self) -> float:
        total = 0
        for meal in self.meals.all():
            total += meal.total_calories
        return total

    @property
    def total_proteins(self) -> float:
        total = 0
        for meal in self.meals.all():
            total += meal.total_proteins
        return total

    @property
    def total_fats(self) -> float:
        total = 0
        for meal in self.meals.all():
            total += meal.total_fats
        return total

    @property
    def total_carbohydrates(self) -> float:
        total = 0
        for meal in self.meals.all():
            total += meal.total_carbohydrates
        return total


