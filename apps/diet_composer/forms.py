from django import forms

from apps.diet_composer.models import Product, ProductItem


class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ["category", "product", "weight", "unit"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['product'].queryset = Product.objects.none()
    #
    #     if 'category' in self.data:
    #         try:
    #             category_id = int(self.data.get('category'))
    #             self.fields['product'].queryset = Product.objects.filter(category_id=category_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['product'].queryset = self.instance.category.product_set.order_by('name')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("author",)
