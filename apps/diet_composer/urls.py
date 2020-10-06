from django.urls import path

from .views import (ProductCreateView)

urlpatterns = [
    path("product/new", ProductCreateView.as_view(), name="product-create")
]
