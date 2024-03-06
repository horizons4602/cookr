import requests
import os
from dotenv import load_dotenv
load_dotenv()

APIKEY = os.getenv('SPOONACULAR_API_KEY')

# Define Recipe Class
class Recipe:
    def __init__(self, id, image, url, name, readyInMinutes, displayIngredients, ingredientNames, instructions, cuisines, cheap, dairyFree, glutenFree, vegan, vegetarian, veryHealthy, veryPopular, healthScore, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness):
        self.id = id
        self.image = image
        self.url = url
        self.name = name
        self.readyInMinutes = readyInMinutes
        self.displayIngredients = displayIngredients
        self.ingredientNames = ingredientNames
        self.instructions = instructions
        self.cuisines = cuisines
        self.cheap = cheap
        self.dairyFree = dairyFree
        self.glutenFree = glutenFree
        self.vegan = vegan
        self.vegetarian = vegetarian
        self.veryHealthy = veryHealthy
        self.veryPopular = veryPopular
        self.healthScore = healthScore
        self.sweetness = sweetness
        self.saltiness = saltiness
        self.sourness = sourness
        self.bitterness = bitterness
        self.savoriness = savoriness
        self.fattiness = fattiness
        self.spiciness = spiciness
    
    def __str__(self):
        return f"ID: {self.id}\nImage {self.image}\nURL: {self.url}\nName: {self.name}\nReady In Minutes: {self.readyInMinutes}\nDisplay Ingredients: {self.displayIngredients}\nIngredient Names: {self.ingredientNames}\nInstructions: {self.instructions}\nCuisines: {self.cuisines}\nCheap: {self.cheap}\nDairy Free: {self.dairyFree}\nGluten Free: {self.glutenFree}\nVegan: {self.vegan}\nVegetarian: {self.vegetarian}\nVery Healthy: {self.veryHealthy}\nVery Popular: {self.veryPopular}\nHealth Score: {self.healthScore}\nSweetness: {self.sweetness}\nSaltiness: {self.saltiness}\nSourness: {self.sourness}\nBitterness: {self.bitterness}\nSavouriness: {self.savoriness}\nFattiness: {self.fattiness}\nSpiciness: {self.spiciness}"

# Get Recipe From API and return Recipe Object (Default params are for random search)
def getRecipe(queryType="random", params=None):
    if (queryType == "random"):
        # Call API for Random Recipe
        results = requests.get('https://api.spoonacular.com/recipes/random?apiKey=' + APIKEY).json()
        id = results['recipes'][0]['id']
        recipe = requests.get('https://api.spoonacular.com/recipes/' + str(id) + '/information?apiKey=' + APIKEY).json()
    elif (queryType == "search"):
        # Call API for Search Recipe
        results = requests.get('https://api.spoonacular.com/recipes/complexSearch?apiKey=' + APIKEY, params=params).json()
        id = results['results'][0]['id']
        recipe = requests.get('https://api.spoonacular.com/recipes/' + str(id) + '/information?apiKey=' + APIKEY).json()
    else:
        print("Invalid queryType parameter:", queryType)
        return

    # Recipe Information
    id = recipe['id']
    image = recipe['image']
    url = recipe['sourceUrl']
    name = recipe['title']
    readyInMinutes = recipe['readyInMinutes']
    ingredients = recipe['extendedIngredients']
    displayIngredients = []
    ingredientNames = []
    for i in ingredients:
        displayIngredients.append(i['original'])
        ingredientNames.append(i['nameClean'])
    instructions = recipe['instructions']
    cuisines = recipe['cuisines']
    cheap = recipe['cheap']
    dairyFree = recipe['dairyFree']
    glutenFree = recipe['glutenFree']
    vegan = recipe['vegan']
    vegetarian = recipe['vegetarian']
    veryHealthy = recipe['veryHealthy']
    veryPopular = recipe['veryPopular']
    healthScore = recipe['healthScore']

    # Call API for Flavor Scorings by Recipe ID
    payload = {'normalize': True}
    flavorScores = requests.get('https://api.spoonacular.com/recipes/' + str(id) + '/tasteWidget.json?apiKey=' + APIKEY, params=payload).json()

    sweetness = flavorScores['sweetness']
    saltiness = flavorScores['saltiness']
    sourness = flavorScores['sourness']
    bitterness = flavorScores['bitterness']
    savoriness = flavorScores['savoriness']
    fattiness = flavorScores['fattiness']
    spiciness = flavorScores['spiciness']

    #Create and Return Recipe Object
    return Recipe(id, image, url, name, readyInMinutes, displayIngredients, ingredientNames, instructions, cuisines, cheap, dairyFree, glutenFree, vegan, vegetarian, veryHealthy, veryPopular, healthScore, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness)

# Test Code with Random Recipe
payload = {'number': 1, 'sort': 'random'}
recipe1 = getRecipe("search", payload)
print(recipe1)