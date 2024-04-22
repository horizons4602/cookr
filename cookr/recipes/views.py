from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Recipe
from accounts.models import UserPreferences, UserAPIkeys, Profile
import requests


# IN THE FUTURE ADD CALORIES PARAMETER
def edamam_api_call(user):
    user_api_keys = UserAPIkeys.objects.get(user=user)
    user_preferences = UserPreferences.objects.get(user=user)
    user_profile = Profile.objects.get(user=user)

    health_labels = []

    for field in UserPreferences._meta.fields:
        if field.name != "user":
            if getattr(user_preferences, field.name):
                health_labels.append(field.name.replace("_", "-").lower())

    if user_profile.goal == 0:
        diet = "balanced"
    elif user_profile.goal == 1:
        diet = "low-carb"
    else:
        diet = "high-protein"

    url = "https://api.edamam.com/api/recipes/v2"

    recipe_data = {
        "Image_Url": [],
        "Name": [],
        "Time": [],
        "Calories": [],
        "Fat": [],
        "Carbs": [],
        "Protein": [],
        "Ingredients": [],
        "SiteUrl": [],
        "Items": 0,
        "Seen": 0,
    }

    params = {
        "type": "public",
        "app_id": user_api_keys.edamam_app_id,
        "app_key": user_api_keys.edamam_api_key,
        "diet": diet,
        "health": health_labels,
        "random": True,
        "field": ["image", "label", "url", "ingredients", "calories", "totalTime", "totalNutrients"],
    }

    response = requests.get(url,params=params)

    if response.status_code == 200:
        data = response.json()
        recipes = data.get('hits', [])

        if recipes:
            for recipe in recipes:
                recipe_info = recipe.get('recipe')
                if recipe_info:
                    name = recipe_info.get('label')
                    image_url = recipe_info.get('image')
                    site_url = recipe_info.get('url')
                    calories = recipe_info.get('calories')
                    time_to_cook = recipe_info.get('totalTime')
                    fat = recipe_info.get('totalNutrients', {}).get('FAT', {}).get('quantity')
                    carbs = recipe_info.get('totalNutrients', {}).get('CHOCDF', {}).get('quantity')
                    protein = recipe_info.get('totalNutrients', {}).get('PROCNT', {}).get('quantity')
                    ingredients_data = recipe_info.get('ingredients', [])
                    ingredients = [ingredient.get('food') for ingredient in ingredients_data]

                    recipe_data["Image_Url"].append(image_url)
                    recipe_data["Name"].append(name)
                    recipe_data["Time"].append(time_to_cook)
                    recipe_data["Calories"].append(calories)
                    recipe_data["Protein"].append(protein)
                    recipe_data["Ingredients"].append(ingredients)
                    recipe_data["SiteUrl"].append(site_url)
                    recipe_data["Fat"].append(fat)
                    recipe_data["Carbs"].append(carbs)
                    recipe_data["Items"] += 1

            return recipe_data
        else:
            print("NONE")
            return "NONE FOUND"


class Main(TemplateView):
    template_name = "recipes/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        recipe_instance, created = Recipe.objects.get_or_create(user=user)

        # Attempt to fetch an unseen recipe
        recipe = recipe_instance.get_next_recipe()

        if not recipe:
            # If no unseen recipes are available, make an API call
            recipe = edamam_api_call(user)
            if recipe != "NONE FOUND":
                recipe_instance.add_recipes(recipe)
                recipe = recipe_instance.get_next_recipe()  # Retrieve the first of the newly added recipes

        # Assign recipe details to the context if available
        if recipe:
            context.update({
                "image": recipe["Image_Url"],
                "name": recipe["Name"],
                "time": recipe["Time"],
                "calories": recipe["Calories"],
                "protein": recipe["Protein"],
                "ingredient": recipe["Ingredients"],
                "fat": recipe["Fat"],
                "carbohydrates": recipe["Carbs"],
                "site": recipe["SiteUrl"],
            })

        return context
