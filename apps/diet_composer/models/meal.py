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
    ingredients = models.ManyToManyField(ProductItem, related_name="ingredients")

    def __str__(self):
        return f"{self.name}"



