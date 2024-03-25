# This class stores everything pertaining to API calls
# To use:
# from edamamrecipeapi import <FUNCTION_NAME>

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from cookr.db import get_db
from cookr.dbhelper import get_user_health_restrictions
from cookr.recipeclasses import Recipe
import random
load_dotenv()

APIKEY_EDAMAM = os.getenv('EDAMAM_API_KEY')
APPID_EDAMAM = os.getenv('EDAMAM_APP_ID')

def random_recipe(query):
    url = "https://api.edamam.com/api/recipes/v2"

    params = {
        "type": "public",
        "q": query,
        "app_id": APPID_EDAMAM,
        "app_key": APIKEY_EDAMAM,
        "random": True
    }

    response = requests.get(url,params=params)

    if response.status_code == 200:
        data = response.json()
        recipes = data.get('hits', [])

        if recipes:
            random_recipe = random.choice(recipes).get('recipe')
            return random_recipe
        else:
            return "NONE FOUND"



# Get Recipe From API and return Recipe Object (Default params are for random search)
def get_recipes(params=None, next=None, user_id=None):

        # Default recipes that can be obtained per API query
        recipesPerQuery = 20

        # Default params
        defaultParams = "?type=public"
        appAuthParams = "&app_id=" + APPID_EDAMAM
        keyAuthParams = "&app_key=" + APIKEY_EDAMAM

        # Continue Existing Query
        if next != None:
            response = requests.get(next)
        else:
            # Get health restrictions
            dietaryRestrictions = get_user_health_restrictions(user_id)
            dietaryRestrictionsParam = {key: True for key, value in dietaryRestrictions.items() if value}
            # params.update(dietaryRestrictionsParam)

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
            return analyze_recipes(resultsQuery, recipesPerQuery)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
     
def analyze_recipes(recipesQuery, recipesPerQuery):
    # Next page
    try:
        next = recipesQuery["_links"]["next"]["href"]
    except:
        # Check for "None" recipes in caller
        return None, None
    
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

        #print(f"Recipe {recipeIndex}:\nTitle: {title}\nCalories: {calories}\nTotal Weight: {totalWeight}\nTotal Time: {totalTime}")

        # Here is where we take all the nutritional info and create our own algorithm for
        # "healthiness" based on user goals, weight, diet, etc.

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

        # Get current time and date, formatted for DATETIME type
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if error is None:
            try:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO recipe (creationTime, selfHref, image, url, title, calories, totalWeight, totalTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (current_datetime, selfHref, image, url, title, calories, totalWeight, totalTime),
                )

                # Get the last inserted row's id
                recipe_id = cursor.lastrowid

                # Database ID for recipe object
                id = recipe_id

                for ingredient in ingredients:
                    cursor.execute(
                        "INSERT INTO ingredient (recipe_ID, name) VALUES (?, ?)",
                        (recipe_id, ingredient),
                    )
                
            except db.IntegrityError:
                # Should not occur, but just in case ¯\_(ツ)_/¯ 
                error = f"Database Error: Recipe {recipe} could not be inserted into Database."
                print(error)
        
        recipe = Recipe(id, selfHref, image, url, title, ingredients, calories, totalWeight, totalTime)
        recipes.append(recipe)


    db.commit()
    #Create and Return Recipe List, Next Link
    return recipes, next