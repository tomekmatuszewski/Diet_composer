from apps.recipes.models import Recipe


def all_recipes(request):
    return {"all_recipes": Recipe.objects.all()}
