from apps.diet_composer.models import ProductItem
from django.db import models


class Meal(models.Model):
    class Name(models.TextChoices):
        breakfast = 'Breakfast'
        lunch = 'Lunch'
        dinner = 'Dinner'
        snack = "Afternoon snack"
        post_workout = 'Post-workout meal'
        supper = "Supper"

    name = models.CharField(choices=Name.choices, max_length=50, null=True, blank=True)
    ingredients = models.ManyToManyField(ProductItem, related_name="meals")

    def __str__(self):
        return f"{self.name} created for {self.menus.all()[0].author}"

    @property
    def total_calories(self):
        total = 0
        for ingredient in self.ingredients.all():
            total += ingredient.calories
        return round(total, 2)

    @property
    def total_proteins(self):
        total = 0
        for ingredient in self.ingredients.all():
            total += ingredient.proteins
        return round(total, 2)

    @property
    def total_fats(self):
        total = 0
        for ingredient in self.ingredients.all():
            total += ingredient.fats
        return round(total, 2)

    @property
    def total_carbohydrates(self):
        total = 0
        for ingredient in self.ingredients.all():
            total += ingredient.carbohydrates
        return round(total, 2)







