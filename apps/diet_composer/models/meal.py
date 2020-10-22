from django.db import models

from apps.diet_composer.utils import calculate_total_value_meal


class Meal(models.Model):
    class Name(models.TextChoices):
        breakfast = "Breakfast"
        lunch = "Lunch"
        dinner = "Dinner"
        snack = "Afternoon snack"
        post_workout = "Post-workout meal"
        supper = "Supper"

    name = models.CharField(choices=Name.choices, max_length=50, unique=True)
    ingredients = models.ManyToManyField(
        "diet_composer.ProductItem", related_name="meals"
    )
    recipes = models.ManyToManyField("diet_composer.RecipeItem", related_name="meals")

    def __str__(self):
        return f"{self.name}"

    def delete(self, using=None, keep_parents=False):
        for ingredient in self.ingredients.all():
            ingredient.delete()
        for recipe in self.recipes.all():
            recipe.delete()
        super().delete()

    @property
    def total_calories(self) -> float:
        value = calculate_total_value_meal(
            self.ingredients.all(), self.recipes.all(), "calories"
        )
        return value

    @property
    def total_proteins(self) -> float:
        value = calculate_total_value_meal(
            self.ingredients.all(), self.recipes.all(), "proteins"
        )
        return value

    @property
    def total_fats(self) -> float:
        value = calculate_total_value_meal(
            self.ingredients.all(), self.recipes.all(), "fats"
        )
        return value

    @property
    def total_carbohydrates(self) -> float:
        value = calculate_total_value_meal(
            self.ingredients.all(), self.recipes.all(), "carbohydrates"
        )
        return value
