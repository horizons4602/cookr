from django.views.generic import TemplateView


class Saved(TemplateView):
	template_name = "favorites/saved.html"
