from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from apps.diet_composer.models import DailyMenu, Meal, Product, ProductItem
from apps.diet_composer.forms import ProductItemForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from apps.diet_composer.utils import check_nutritional_status


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("create-menu")


class ProductItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    template_name = "diet_composer/productitem_form.html"
    form_class = ProductItemForm
    success_message = "Ingredient added to meal"

    def form_valid(self, form):
        menu = DailyMenu.objects.get(id=self.kwargs["menu_id"])
        meal = Meal.objects.get(id=self.kwargs["meal_id"])
        if form.is_valid():
            category = form.cleaned_data["category"]
            product = form.cleaned_data["product"]
            weight = form.cleaned_data["weight"]
            unit = form.cleaned_data["unit"]
            ingredient = ProductItem(category=category, product=product, weight=weight, unit=unit)
            if check_nutritional_status(self.request.user, menu, ingredient):
                ingredient.save()
                meal.ingredients.add(ingredient)
                messages.success(self.request, message=f"Successfully added ingredient to {meal.name}")
            else:
                messages.error(self.request, message="The nutritional value of your menu has exceeded your personal limit")
        return HttpResponseRedirect(reverse_lazy("menu-details", args=[self.kwargs["menu_id"]]))


class ProductItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = "diet_composer/productitem_form.html"
    form_class = ProductItemForm
    model = ProductItem

    def get_success_url(self):
        return reverse_lazy("menu-details", kwargs={"pk": self.kwargs["menu_id"]})

    def get_success_message(self, cleaned_data):
        return f"Successfully edited ingredient: {cleaned_data['product'].name}"


class ProductItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = ProductItem

    def get_success_url(self):
        return reverse_lazy("menu-details", kwargs={"pk": self.kwargs["menu_id"]})

    def test_func(self):
        menu = DailyMenu.objects.get(id=self.kwargs["menu_id"])
        if self.request.user == menu.author:
            return True
        return False


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


class MenuUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DailyMenu
    fields = ["name", "number_of_meals"]
    template_name = "diet_composer/create_menu.html"

    def get_success_message(self, cleaned_data):
        return f"Successfully edited menu: {cleaned_data['name']}"

    def get_success_url(self):
        return reverse_lazy("user-menus", kwargs={"username": self.object.author.username})


class MenuDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = DailyMenu
    template_name = "diet_composer/menu_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("user-menus", kwargs={"username": self.object.author.username})

    def test_func(self):
        menu = self.get_object()
        if self.request.user == menu.author:
            return True
        return False


class MealCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Meal
    fields = ["name"]
    success_message = "Succesfully added meal to your Menu"

    def form_valid(self, form):
        menu = DailyMenu.objects.get(id=self.kwargs["pk"])
        if form.is_valid() and menu.meals.count() < menu.number_of_meals:
            name = form.cleaned_data['name']
            meal = Meal(name=name)
            meal.save()
            menu.meals.add(meal)
            messages.success(self.request, message="Succesfully added meal to your Menu")
        else:
            messages.error(self.request, message=f"Max number of meals achieved for {menu.name}")
        return HttpResponseRedirect(reverse_lazy("menu-details", args=[self.kwargs["pk"]]))









