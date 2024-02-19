# This class stores everything pertaining to API calls
# To use:
# from recipeapi import <FUNCTION_NAME>

import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

from cookr.edamamrecipeapi import Recipe

APIKEY_SPOONACULAR = os.getenv('SPOONACULAR_API_KEY')
    
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

class RecipeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Recipe):
            return obj.__dict__
        return super().default(obj)

def limit(num):
     if num > 100:
        return 100
     if num < 0:
        return 0

def get_recipe_desc(recipe, params=None):
    # Call API for Flavor Scorings by Recipe ID
    recipe_json = json.dumps(recipe, cls=RecipeEncoder)
    flavorScores = requests.post('https://api.spoonacular.com/recipes/analyze?includeTaste=True' + APIKEY_SPOONACULAR, 
                                 json=recipe_json, params=params).json()

    sweetness = limit(flavorScores['sweetness'])
    saltiness = limit(flavorScores['saltiness'])
    sourness = limit(flavorScores['sourness'])
    bitterness = limit(flavorScores['bitterness'])
    savoriness = limit(flavorScores['savoriness'])
    fattiness = limit(flavorScores['fattiness'])
    spiciness = limit(flavorScores['spiciness'])

    return RecipeDesc(id, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness)