from django.db import models

from apps.diet_composer.utils import calculate_recipe_nutri


class RecipeItem(models.Model):

    recipe_category = models.ForeignKey("recipes.Category", on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipes.Recipe", on_delete=models.CASCADE)
    piece = models.DecimalField(max_digits=3, decimal_places=1, max_length=150)

    def __str__(self):
        return f"{self.recipe.title} item"

    @property
    def calories(self) -> float:
        calories = calculate_recipe_nutri(self.recipe.total_calories, self.piece)
        return calories

    @property
    def proteins(self) -> float:
        proteins = calculate_recipe_nutri(self.recipe.total_proteins, self.piece)
        return proteins

    @property
    def fats(self) -> float:
        fats = calculate_recipe_nutri(self.recipe.total_fats, self.piece)
        return fats

    @property
    def carbohydrates(self) -> float:
        carbohydrates = calculate_recipe_nutri(
            self.recipe.total_carbohydrates, self.piece
        )
        return carbohydrates
