from django.contrib import admin

from apps.diet_composer.models import (DailyMenu, Meal, Product,
                                       ProductCategory, ProductItem)

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductItem)
admin.site.register(Meal)
admin.site.register(DailyMenu)
