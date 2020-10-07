from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from apps.diet_composer.models import DailyMenu, Meal, Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("diet-composer")


class MultipleModelView(LoginRequiredMixin, CreateView):

    template_name = "diet_composer/diet_composer.html"
    model = DailyMenu
    fields = "__all__"

