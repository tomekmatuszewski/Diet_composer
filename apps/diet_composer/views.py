from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from apps.diet_composer.models import DailyMenu, Meal, Product, ProductItem
from apps.diet_composer.forms import ProductItemForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("create-menu")


class ProductItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    template_name = "diet_composer/productitem_form.html"
    form_class = ProductItemForm
    success_message = "Ingredient added to meal"

    # def form_valid(self, form):
    #     menu = DailyMenu.objects.get(id=self.kwargs["pk"])
    #     if menu.meals.count() < menu.number_of_meals:
    #         name = form.cleaned_data['name']
    #         meal = Meal(name=name)
    #         meal.save()
    #         menu.meals.add(meal)
    #         messages.success(self.request, message="Succesfully added meal to your Menu")
    #     else:
    #         messages.error(self.request, message="Max number of meals achieved")
    #     return HttpResponseRedirect(reverse_lazy("menu-details", args=[self.kwargs["pk"]]))


def load_products(request):
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'diet_composer/product_dropdown_list_options.html', {'products': products})


class UserMenuListView(ListView):
    model = DailyMenu
    template_name = "diet_composer/user_menus.html"
    context_object_name = "menus"
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return DailyMenu.objects.filter(author=user)


class MenuCreateView(LoginRequiredMixin, CreateView):

    template_name = "diet_composer/create_menu.html"
    model = DailyMenu
    fields = ["name", "number_of_meals"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("user-menus", kwargs={"username": self.object.author.username})


class MenuDetailView(DetailView):

    model = DailyMenu
    template_name = "diet_composer/menu_detail.html"


class MealCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Meal
    fields = ["name"]
    success_message = "Succesfully added meal to your Menu"

    def form_valid(self, form):
        menu = DailyMenu.objects.get(id=self.kwargs["pk"])
        if menu.meals.count() < menu.number_of_meals:
            name = form.cleaned_data['name']
            meal = Meal(name=name)
            meal.save()
            menu.meals.add(meal)
            messages.success(self.request, message="Succesfully added meal to your Menu")
        else:
            messages.error(self.request, message="Max number of meals achieved")
        return HttpResponseRedirect(reverse_lazy("menu-details", args=[self.kwargs["pk"]]))







