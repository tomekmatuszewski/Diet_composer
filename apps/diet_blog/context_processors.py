from apps.diet_blog.models import Post


def all_posts(request):
    return {"all_posts": Post.objects.all()}
