from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView
from apps.diet_composer.models import Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = "__all__"
