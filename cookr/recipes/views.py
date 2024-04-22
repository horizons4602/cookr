from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Recipe
from accounts.models import UserPreferences, UserAPIkeys, Profile, UserAllergies
import requests


def edamam_api_call(user):
    try:
        user_api_keys = UserAPIkeys.objects.get(user=user)
        user_preferences = UserAllergies.objects.get(user=user)
        user_profile = Profile.objects.get(user=user)
        health_labels = []
        for field in UserAllergies._meta.fields:
            if field.name != "user" and getattr(user_preferences, field.name):
                health_labels.append(field.name.replace("_", "-").lower())

        if user_profile.goal == 0:
            diet = "balanced"
        elif user_profile.goal == 1:
            diet = "low-carb"
        else:
            diet = "high-protein"

        url = "https://api.edamam.com/api/recipes/v2"
        params = {
            "type": "public",
            "app_id": user_api_keys.edamam_app_id,
            "app_key": user_api_keys.edamam_api_key,
            "diet": diet,
            "health": health_labels,
            "random": True,
            "field": ["image", "label", "url", "ingredients", "calories", "totalTime", "totalNutrients"],
        }

        print(params)

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return "API_CALL_FAILED"

        data = response.json()
        recipes = data.get('hits', [])
        if not recipes:
            return "NONE FOUND"

        recipe_data = {"Image_Url": [], "Name": [], "Time": [], "Calories": [], "Fat": [], "Carbs": [], "Protein": [],
                       "Ingredients": [], "SiteUrl": [], "Items": 0, "Seen": 0}
        for recipe in recipes:
            recipe_info = recipe.get('recipe')
            if recipe_info:
                recipe_data["Image_Url"].append(recipe_info.get('image'))
                recipe_data["Name"].append(recipe_info.get('label'))
                recipe_data["Time"].append(recipe_info.get('totalTime'))
                recipe_data["Calories"].append(recipe_info.get('calories'))
                recipe_data["Protein"].append(recipe_info.get('totalNutrients', {}).get('PROCNT', {}).get('quantity'))
                recipe_data["Ingredients"].append(
                    [ingredient.get('food') for ingredient in recipe_info.get('ingredients', [])])
                recipe_data["SiteUrl"].append(recipe_info.get('url'))
                recipe_data["Fat"].append(recipe_info.get('totalNutrients', {}).get('FAT', {}).get('quantity'))
                recipe_data["Carbs"].append(recipe_info.get('totalNutrients', {}).get('CHOCDF', {}).get('quantity'))
                recipe_data["Items"] += 1

        return recipe_data

    except UserAPIkeys.DoesNotExist:
        return "API_KEY_MISSING"  # Handle the case where API keys are missing


class Main(TemplateView):
    template_name = "recipes/main.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        recipe_instance, created = Recipe.objects.get_or_create(user=user)
        recipe = recipe_instance.get_next_recipe()

        if not recipe:
            recipe_data = edamam_api_call(user)
            if recipe_data in ["API_KEY_MISSING", "API_CALL_FAILED", "NONE FOUND"]:
                # Return a different response if there's an issue with API keys or API call
                return render(request, "recipes/error_template.html", {"error": recipe_data})

            recipe_instance.add_recipes(recipe_data)
            recipe = recipe_instance.get_next_recipe()

        if recipe:
            context = {
                "image": recipe["Image_Url"],
                "name": recipe["Name"],
                "time": recipe["Time"],
                "calories": round(recipe["Calories"]),
                "protein": round(recipe["Protein"]),
                "ingredient": recipe["Ingredients"],
                "fat": round(recipe["Fat"]),
                "carbohydrates": round(recipe["Carbs"]),
                "site": recipe["SiteUrl"],
            }
        else:
            context = {}

        context = self.get_context_data(**context)
        return self.render_to_response(context)
