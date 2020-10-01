from apps.recipes.models import Recipe


def all_recipes(request):
    common_tags = Recipe.tags.most_common()
    return {"all_recipes": Recipe.objects.all(), "common_tags": common_tags}
