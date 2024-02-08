# This class stores everything pertaining to API calls
# To use:
# from edamamrecipeapi import <FUNCTION_NAME>

import requests
import os
from dotenv import load_dotenv
load_dotenv()

APIKEY_EDAMAM = os.getenv('EDAMAM_API_KEY')
APPID_EDAMAM = os.getenv('EDAMAM_APP_ID')

# Define Recipe Class
class Recipe:
    def __init__(self, id, image, url, title, ingredients, calories, totalWeight, totalTime):
        self.id = id
        self.image = image
        self.url = url
        self.title = title
        self.ingredients = ingredients
        self.calories = calories
        self.totalWeight = totalWeight
        self.totalTime = totalTime
    
    def __str__(self):
        return f"ID: {self.id}\nImage {self.image}\nURL: {self.url}\nTitle: {self.title}\nIngredients: {self.ingredients}\nCalories: {self.calories}\nTotal Weight: {self.totalWeight}\nTotal Time: {self.totalTime}"

# Get Recipe From API and return Recipe Object (Default params are for random search)
def get_recipes(params=None):
        # Replace offset system with REST API links they have
        
        # Default params
        defaultParams = "?app_key = " + APIKEY_EDAMAM + "&app_id_param=" + APPID_EDAMAM + "&type=public&random=true&"
        # Call API for Search Recipe
        resultsQuery = requests.get('https://api.spoonacular.com/recipes/complexSearch' + defaultParams, 
                                    params=params).json()
        if 'code' in resultsQuery.keys():
            if resultsQuery['code'] != 200:
                if resultsQuery['code'] == 402:
                    return "Out of API Calls"

        numResults = resultsQuery['count']
        if numResults == 0:
            # Frontend handles this :)
            return "No Recipes Found"
        # For when there are less recipes than searched for
        recipesPerQuery = min(numResults, recipesPerQuery)
        return analyze_recipes(resultsQuery, recipesPerQuery)

def limit(num):
     if num > 100:
        return 100
     if num < 0:
        return 0
     
def analyze_recipes(recipesQuery, recipesPerQuery):
    # List of anaylyzed recipe information
    recipes = []
    for recipeIndex in range(1, recipesPerQuery - 1):
    # Recipe Information
        id = recipesQuery["hits"][recipeIndex]["recipe"]['id']
        image = recipesQuery["hits"][recipeIndex]["recipe"]['label']
        url = recipesQuery["hits"][recipeIndex]["recipe"]['url']
        title = recipesQuery["hits"][recipeIndex]["recipe"]['image']
        ingredients = []
        for ingredient in recipesQuery["hits"][recipeIndex]["recipe"]["ingredientLines"]:
            ingredients.append(ingredient)
        calories = recipesQuery["hits"][recipeIndex]["recipe"]['calories']
        totalWeight = recipesQuery["hits"][recipeIndex]["recipe"]['totalWeight']
        totalTime = recipesQuery["hits"][recipeIndex]["recipe"]['totalTime']
        # Get additional nutritional information here, it's in the API call

        # Here is where we take all the nutritional info and create our own algorithm for
        # "healthiness" based on user goals, weight, diet, etc.

        recipes.append(Recipe(id, image, url, title, ingredients, calories, totalWeight, totalTime))

    #Create and Return Recipe List
    return recipes