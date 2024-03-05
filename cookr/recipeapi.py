# This class stores everything pertaining to API calls
# To use:
# from recipeapi import <FUNCTION_NAME>

import requests
import os
import json
from dotenv import load_dotenv
from cookr.recipeclasses import RecipeDesc
load_dotenv()

from cookr.edamamrecipeapi import Recipe

APIKEY_SPOONACULAR = os.getenv('SPOONACULAR_API_KEY')

def RecipeEncoder(recipe):
    recipe_data = {
        "title": recipe.title,
        "ingredients": recipe.ingredients,
    }

    json_data = json.dumps(recipe_data)

    return json_data

def limit(num):
    if isinstance(num, float):
        return max(0.0, min(num, 100.0))
    elif isinstance(num, int):
        return max(0, min(num, 100))


def get_recipe_desc(recipe):
    # Call API for Flavor Scorings by Recipe ID
    recipe_json_post = RecipeEncoder(recipe)

    keyAuthParams = "&apiKey=" + APIKEY_SPOONACULAR

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.post('https://api.spoonacular.com/recipes/analyze?includeTaste=True' + keyAuthParams, 
                             data=recipe_json_post, headers=headers)

    try:
        analyzeRecipeQuery = response.json()
        sweetness = limit(analyzeRecipeQuery['taste']['sweetness'])
        saltiness = limit(analyzeRecipeQuery['taste']['saltiness'])
        sourness = limit(analyzeRecipeQuery['taste']['sourness'])
        bitterness = limit(analyzeRecipeQuery['taste']['bitterness'])
        savoriness = limit(analyzeRecipeQuery['taste']['savoriness'])
        fattiness = limit(analyzeRecipeQuery['taste']['fattiness'])
        spiciness = limit(analyzeRecipeQuery['taste']['spiciness'])
        
        recipeDesc = RecipeDesc(sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness)
        return recipeDesc
    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print(f"Error in HTTP reponse code?: {response.status_code}")
        print(f"Response text: {response.text}")