# This class stores everything pertaining to API calls
# To use:
# from recipeapi import <FUNCTION_NAME>

import requests
import os
from dotenv import load_dotenv
load_dotenv()

APIKEY = os.getenv('SPOONACULAR_API_KEY')

# Define Recipe Class
class Recipe:
    def __init__(self, id, image, url, title, ingredientNames, instructions, cheap, dairyFree, glutenFree, vegan, vegetarian, veryHealthy, veryPopular, healthScore):
        self.id = id
        self.image = image
        self.url = url
        self.title = title
        self.ingredientNames = ingredientNames
        self.instructions = instructions
        self.cheap = cheap
        self.dairyFree = dairyFree
        self.glutenFree = glutenFree
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.veryHealthy = veryHealthy
        self.veryPopular = veryPopular
        self.healthScore = healthScore
    
    def __str__(self):
        return f"ID: {self.id}\nImage {self.image}\nURL: {self.url}\nTitle: {self.title}\nIngredients: {self.ingredientNames}\nInstructions: {self.instructions}\nCheap: {self.cheap}\nDairy Free: {self.dairyFree}\nGluten Free: {self.glutenFree}\nVegan: {self.vegan}\nVegetarian: {self.vegetarian}\nVery Healthy: {self.veryHealthy}\nVery Popular: {self.veryPopular}\nHealth Score: {self.healthScore}\nSweetness: {self.sweetness}\nSaltiness: {self.saltiness}\nSourness: {self.sourness}\nBitterness: {self.bitterness}\nSavouriness: {self.savoriness}\nFattiness: {self.fattiness}\nSpiciness: {self.spiciness}"
    
class RecipeDesc:
        def __init__(self, id, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness):
            self.id = id
            self.sweetness = sweetness
            self.saltiness = saltiness
            self.sourness = sourness
            self.bitterness = bitterness
            self.savoriness = savoriness
            self.fattiness = fattiness
            self.spiciness = spiciness
        def __str__(self):
            return f"ID: {self.id}\nSweetness: {self.sweetness}\nSaltiness: {self.saltiness}\nSourness: {self.sourness}\nBitterness: {self.bitterness}\nSavouriness: {self.savoriness}\nFattiness: {self.fattiness}\nSpiciness: {self.spiciness}"

# Get Recipe From API and return Recipe Object (Default params are for random search)
def get_recipes(params=None):
        if 'offset' in params.keys():
            if params["offset"] > 900:
                return "Out of Recipes"
        
        recipesPerQuery = 100
        # Call API for Search Recipe
        resultsQuery = requests.get('https://api.spoonacular.com/recipes/complexSearch?apiKey=' + APIKEY + '&number=' + str(recipesPerQuery), params=params).json()
        if 'code' in resultsQuery.keys():
            if resultsQuery['code'] != 200:
                if resultsQuery['code'] == 402:
                    return "Out of API Calls"


        print(resultsQuery)
        numResults = resultsQuery['totalResults']
        if numResults == 0:
            # Frontend handles this
            return "No Recipes Found"
        # For when there is less recipes than searched for
        recipesPerQuery = min(numResults, recipesPerQuery)
        # Create Bulk ID String
        bulkIds = str(resultsQuery['results'][0]['id'])
        for recipe in range(1, recipesPerQuery):
            print(recipe)
            bulkIds += "," + str(resultsQuery['results'][recipe]['id'])
        analyze_recipes(bulkIds, recipesPerQuery)

def limit(num):
     if num > 100:
        return 100
     if num < 0:
        return 0

def analyze_recipes(bulkIds, recipesPerQuery):
    recipesQuery = requests.get('https://api.spoonacular.com/recipes/informationBulk?' + 'ids=' + bulkIds + '&apiKey=' + APIKEY).json()
    # List of anaylyzed recipe information
    recipes = []
    for recipe in range (0, recipesPerQuery - 1):
    # Recipe Information
        id = recipesQuery[recipe]['id']
        image = recipesQuery[recipe]['image']
        url = recipesQuery[recipe]['sourceUrl']
        title = recipesQuery[recipe]['title']
        ingredients = recipesQuery[recipe]['extendedIngredients']
        ingredientNames = []
        for ingredient in ingredients:
            ingredientNames.append(ingredient['original'])
        instructions = recipesQuery[recipe]['instructions']
        cheap = recipesQuery[recipe]['cheap']
        dairyFree = recipesQuery[recipe]['dairyFree']
        glutenFree = recipesQuery[recipe]['glutenFree']
        vegan = recipesQuery[recipe]['vegan']
        vegetarian = recipesQuery[recipe]['vegetarian']
        veryHealthy = recipesQuery[recipe]['veryHealthy']
        veryPopular = recipesQuery[recipe]['veryPopular']
        healthScore = recipesQuery[recipe]['healthScore']

        recipes.append(Recipe(id, image, url, title, ingredientNames, instructions, cheap, dairyFree, glutenFree, vegan, vegetarian, veryHealthy, veryPopular, healthScore))

    #Create and Return Recipe List
    return recipes

def get_recipe_desc(recipe_id, params=None):
    # Call API for Flavor Scorings by Recipe ID
    flavorScores = requests.get('https://api.spoonacular.com/recipes/' + str(id) + '/tasteWidget.json?apiKey=' + APIKEY, params=params).json()

    sweetness = limit(flavorScores['sweetness'])
    saltiness = limit(flavorScores['saltiness'])
    sourness = limit(flavorScores['sourness'])
    bitterness = limit(flavorScores['bitterness'])
    savoriness = limit(flavorScores['savoriness'])
    fattiness = limit(flavorScores['fattiness'])
    spiciness = limit(flavorScores['spiciness'])

    return RecipeDesc(id, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness)

# Search for Vegan Dessert  
payload = {'diet': 'vegan', 'type': 'dessert'}
recipe1 = get_recipes(payload)
print(recipe1)
print(recipe1.image)