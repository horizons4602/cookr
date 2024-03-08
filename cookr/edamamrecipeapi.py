# This class stores everything pertaining to API calls
# To use:
# from edamamrecipeapi import <FUNCTION_NAME>

import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from cookr.db import get_db
from cookr.dbhelper import get_user_health_restrictions, insert_recipe_cache
from cookr.recipeclasses import Recipe
load_dotenv()

APIKEY_EDAMAM = os.getenv('EDAMAM_API_KEY')
APPID_EDAMAM = os.getenv('EDAMAM_APP_ID')

# Get Recipe From API and return Recipe Object (Default params are for random search)
def get_recipes(params=None, user_id=None):

        # Default recipes that can be obtained per API query
        recipesPerQuery = 20

        # Default params
        defaultParams = "?type=public&random=true"
        appAuthParams = "&app_id=" + APPID_EDAMAM
        keyAuthParams = "&app_key=" + APIKEY_EDAMAM

        # Get health restrictions
        dietaryRestrictions = get_user_health_restrictions(user_id)
        dietaryRestrictionsParam = {key: True for key, value in dietaryRestrictions.items() if value}
        params.update(dietaryRestrictionsParam)

        response = requests.get('https://api.edamam.com/api/recipes/v2' + defaultParams + appAuthParams +
                                keyAuthParams, params=params)

        # Check for errors
        if response.status_code == 200:
            resultsQuery = response.json()

            numResults = resultsQuery['count']
            
            if numResults == 0:
                raise Exception("Out of Recipes")
            
            # For when there are less recipes than searched for
            recipesPerQuery = min(numResults, recipesPerQuery)
            return analyze_recipes(resultsQuery, recipesPerQuery, user_id)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
     
def analyze_recipes(recipesQuery, recipesPerQuery, user_id):
    
    # List of anaylyzed recipe information
    recipes = []
    # Connect to the database 
    db = get_db()
    for recipeIndex in range(0, recipesPerQuery):
    # Recipe Information
        selfHref = recipesQuery["hits"][recipeIndex]["_links"]["self"]['href']
        image = recipesQuery["hits"][recipeIndex]["recipe"]['image']
        url = recipesQuery["hits"][recipeIndex]["recipe"]['url']
        title = recipesQuery["hits"][recipeIndex]["recipe"]['label']
        ingredients = []
        for ingredient in recipesQuery["hits"][recipeIndex]["recipe"]["ingredientLines"]:
            ingredients.append(ingredient)
        calories = recipesQuery["hits"][recipeIndex]["recipe"]['calories']
        totalWeight = recipesQuery["hits"][recipeIndex]["recipe"]['totalWeight']
        totalTime = float(recipesQuery["hits"][recipeIndex]["recipe"]['totalTime'])
        # Get additional nutritional information here, it's in the API call

        error = None
        # Check for required fields (probably a better way to do this with list comprehension)
        if selfHref is None:
            error = 'selfHref is required.'
        elif url is None:
            error = 'url is required.'
        elif title is None:
            error = 'title is required.'
        elif ingredients is None:
            error = 'ingredients are required.'
        elif calories is None:
            error = 'calories are required.'
        elif totalWeight is None:
            error = 'totalWeight is required.'
        elif totalTime is None:
            error = 'totalTime is required.'

        # If error, skip to next recipe
        if error is not None:
            continue

        # If recipe already seen by user, skip to next recipe
        existing_recipe = db.execute("SELECT title FROM recipe WHERE title = ? AND saving_user = ?", (title, user_id)).fetchone()
        if existing_recipe is None:
            if error is None:
                try:
                    caching_recipe = recipe = Recipe(id=None, selfHref=selfHref, image=image, url=url, title=title, ingredients=ingredients, calories=calories, 
                                                  totalWeight=totalWeight, totalTime=totalTime)
                    id = insert_recipe_cache(caching_recipe, user_id)
                    recipe = Recipe(id, selfHref, image, url, title, ingredients, calories, totalWeight, totalTime)
                except Exception as e:
                    # Should not occur, but just in case ¯\_(ツ)_/¯ 
                    error = f"Error caching recipe: {recipe.title}, {e}"
                    print(e)
            recipes.append(recipe)
        else:
            continue


    #Create and Return Recipe List
    return recipes