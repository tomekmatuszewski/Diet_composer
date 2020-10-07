from django.urls import path

from .views import (ProductCreateView, MultipleModelView)

urlpatterns = [
    path("product/new", ProductCreateView.as_view(), name="product-create"),
    path("diet-composer/", MultipleModelView.as_view(), name="diet-composer")
]
