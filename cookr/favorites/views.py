from django.views.generic import TemplateView
from .models import SavedOne, SavedTwo, SavedThree, SavedFour, SavedFive, SavedSix
from recipes.models import Recipe
from django.shortcuts import redirect
from .forms import RecipeReplaceForm
from django.http import HttpResponse


class Saved(TemplateView):
	template_name = "favorites/saved.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		Saved_One = user.saved_one
		Saved_Two = user.saved_two
		Saved_Three = user.saved_three
		Saved_Four = user.saved_four
		Saved_Five = user.saved_five
		Saved_Six = user.saved_six

		context["url1"] = Saved_One.image_url
		context["url2"] = Saved_Two.image_url
		context["url3"] = Saved_Three.image_url
		context["url4"] = Saved_Four.image_url
		context["url5"] = Saved_Five.image_url
		context["url6"] = Saved_Six.image_url

		context["savedName1"] = Saved_One.name
		context["savedName2"] = Saved_Two.name
		context["savedName3"] = Saved_Three.name
		context["savedName4"] = Saved_Four.name
		context["savedName5"] = Saved_Five.name
		context["savedName6"] = Saved_Six.name

		context["savedLink1"] = Saved_One.site_url
		context["savedLink2"] = Saved_Two.site_url
		context["savedLink3"] = Saved_Three.site_url
		context["savedLink4"] = Saved_Four.site_url
		context["savedLink5"] = Saved_Five.site_url
		context["savedLink6"] = Saved_Six.site_url

		return context



class SaveRecipe(TemplateView):
	template_name = "favorites/option.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		recipe_instance, created = Recipe.objects.get_or_create(user=user)

		# Attempt to fetch an unseen recipe
		recipe = recipe_instance.get_current_recipe()

		context = super().get_context_data(**kwargs)
		context['form'] = RecipeReplaceForm()
		context['URL'] = recipe["SiteUrl"]

		return context

	def post(self, request, *args, **kwargs):
		form = RecipeReplaceForm(request.POST)
		if form.is_valid():
			recipe_choice = form.cleaned_data['recipe_choice']
			context = super().get_context_data(**kwargs)
			user = self.request.user
			recipe_instance, created = Recipe.objects.get_or_create(user=user)

			# Attempt to fetch an unseen recipe
			recipe = recipe_instance.get_current_recipe()

			if recipe_choice == "saved_one":
				recipe_instance = user.saved_one
			elif recipe_choice == "saved_two":
				recipe_instance = user.saved_two
			elif recipe_choice == "saved_three":
				recipe_instance = user.saved_three
			elif recipe_choice == "saved_four":
				recipe_instance = user.saved_four
			elif recipe_choice == "saved_five":
				recipe_instance = user.saved_five
			elif recipe_choice == "saved_six":
				recipe_instance = user.saved_six
			else:
				return HttpResponse("ERROR Not a valid saved slot")

			if recipe:
				recipe_instance.name = recipe["Name"]
				recipe_instance.image_url = recipe["Image_Url"]
				recipe_instance.site_url = recipe["SiteUrl"]
				recipe_instance.calories = recipe["Calories"]
				recipe_instance.time_to_cook = recipe["Time"]
				recipe_instance.fat = recipe["Fat"]
				recipe_instance.carbs = recipe["Carbs"]
				recipe_instance.protein = recipe["Protein"]
				recipe_instance.ingredients = recipe["Ingredients"]

				recipe_instance.save()
			else:
				return HttpResponse("No Recipe")

		return redirect("saved")
