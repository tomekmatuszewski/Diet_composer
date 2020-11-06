from django.views.generic.base import TemplateView


class HomeView(TemplateView):

    template_name = "home.html"
    extra_context = {"title": "Home"}


class AboutView(TemplateView):

    template_name = "about.html"
    extra_context = {"title": "About"}
