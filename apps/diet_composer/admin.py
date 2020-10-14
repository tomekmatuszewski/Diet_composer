from django.contrib import admin

from apps.diet_composer.models import (DailyMenu, Meal, Product,
                                       ProductCategory, ProductItem,
                                       RecipeItem)

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductItem)
admin.site.register(Meal)
admin.site.register(DailyMenu)
admin.site.register(RecipeItem)
