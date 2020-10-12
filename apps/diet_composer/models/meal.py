from apps.diet_composer.models import ProductItem
from django.db import models
from apps.diet_composer.utils import calculate_total_value_meal


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
        value = calculate_total_value_meal(self.ingredients.all(), "calories")
        return value

    @property
    def total_proteins(self):
        value = calculate_total_value_meal(self.ingredients.all(), "proteins")
        return value

    @property
    def total_fats(self):
        value = calculate_total_value_meal(self.ingredients.all(), "fats")
        return value

    @property
    def total_carbohydrates(self):
        value = calculate_total_value_meal(self.ingredients.all(), "carbohydrates")
        return value







