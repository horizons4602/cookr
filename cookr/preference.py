# Calculating, updating, and querying user preferences

from cookr.dbhelper import get_user_preferences, update_user_preferences, get_user_macronutrients
from cookr.recipeclasses import RecipeDesc, Recipe, RecipeRecommendation

def update_preferences(user_id, recipedesc: RecipeDesc, accept: bool):
    # Based on TCP EstimatedRTT formula
    _alpha = 0.125

    # Check existing user preferences
    user_preferences = get_user_preferences(user_id)

    # First Recipe Ever
    if user_preferences == None:
        user_preferences = recipedesc

    # Update user preferences
    if accept:
        for key in recipedesc:
            user_preferences[key] = (1 - _alpha) * user_preferences[key] + _alpha * recipedesc[key]
    else:
        for key in recipedesc:
            user_preferences[key] = (1 - _alpha) * user_preferences[key] - _alpha * recipedesc[key]

    # Commit changes to database
    update_user_preferences(user_id, user_preferences) 

def recommendation(user_id, recipedesc: RecipeDesc, recipe: Recipe):
    # Recommended taste if within 15% of user preference
    _margin_of_acceptance = 15

    # Get user preferences
    user_preferences = get_user_preferences(user_id)

    # Get user macronutrient preferences
    user_macronutrients = get_user_macronutrients(user_id)

    # Calculate the similarity score
    sweetness = True if abs(user_preferences.sweetness - recipedesc.sweetness) < _margin_of_acceptance else False
    saltiness = True if abs(user_preferences.saltiness - recipedesc.saltiness) < _margin_of_acceptance else False
    sourness = True if abs(user_preferences.sourness - recipedesc.sourness) < _margin_of_acceptance else False
    bitterness = True if abs(user_preferences.bitterness - recipedesc.bitterness) < _margin_of_acceptance else False
    savoriness = True if abs(user_preferences.savoriness - recipedesc.savoriness) < _margin_of_acceptance else False
    fattiness = True if abs(user_preferences.fattiness - recipedesc.fattiness) < _margin_of_acceptance else False
    spiciness = True if abs(user_preferences.spiciness - recipedesc.spiciness) < _margin_of_acceptance else False

    # Calculate percentage of daily values
    calories = round((recipe.calories / user_macronutrients['user_calories']) * 100, 2)
    protein = round((recipe.protein / user_macronutrients['user_protein']) * 100, 2)
    carbs = round((recipe.carbs / user_macronutrients['user_carbs']) * 100, 2)
    fat = round((recipe.fat / user_macronutrients['user_fat']) * 100, 2)
    sugar = round((recipe.sugar / user_macronutrients['user_sugar']) * 100, 2)
    sodium = round((recipe.sodium / user_macronutrients['user_sodium']) * 100, 2)

    # Return the recommendation object
    recommendations = RecipeRecommendation(sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness, calories, protein, carbs, fat, sugar, sodium)
    return recommendations
