from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.diet_composer.utils import calculate_total_value_menu


class DailyMenu(models.Model):

    name = models.CharField(max_length=150)
    number_of_meals = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(6), MinValueValidator(1)]
    )
    meals = models.ManyToManyField(
        "diet_composer.Meal", related_name="menus", blank=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_menus"
    )

    def __str__(self):
        return f"Daily Menu {self.name} created by {self.author.username}"

    @property
    def total_calories(self) -> float:
        value = calculate_total_value_menu(self.meals.all(), "calories")
        return value

    @property
    def total_proteins(self) -> float:
        value = calculate_total_value_menu(self.meals.all(), "proteins")
        return value

    @property
    def total_fats(self) -> float:
        value = calculate_total_value_menu(self.meals.all(), "fats")
        return value

    @property
    def total_carbohydrates(self) -> float:
        value = calculate_total_value_menu(self.meals.all(), "carbohydrates")
        return value

    def delete(self, using=None, keep_parents=False):
        for meal in self.meals.all():
            for product in meal.ingredients.all():
                product.delete()
            for recipe in meal.recipes.all():
                recipe.delete()
            meal.delete()
        super().delete()
