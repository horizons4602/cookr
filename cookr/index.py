from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort

from functools import wraps
from cookr.auth import login_required
from cookr.db import get_db
from cookr.dbhelper import get_recipes_from_ids, get_single_recipe_from_id, get_recipedesc_from_id, insert_recipedesc_cache
from cookr.edamamrecipeapi import get_recipes, random_recipe
from cookr.recipeapi import get_recipe_desc
from cookr.recipeclasses import Recipe, RecipeRecommendation
from cookr.preference import update_preferences, recommendation

import json

bp = Blueprint('index', __name__)

def get_random_recipe():
    recipe_data = random_recipe('salmon')  # Assuming this function fetches recipe data correctly
    recipe_name = recipe_data["label"]

    # Extracting Recipe ID from URI
    uri = recipe_data["uri"]
    recipe_id = uri.split("#recipe_")[1]

    # Extracting Serving Size
    serving_size = recipe_data["yield"]

    macros = {
        "Calories": round(recipe_data["totalNutrients"]["ENERC_KCAL"]["quantity"], 2),
        "Fat": round(recipe_data["totalNutrients"]["FAT"]["quantity"], 2),
        "Carbohydrates": round(recipe_data["totalNutrients"]["CHOCDF"]["quantity"], 2),
        "Protein": round(recipe_data["totalNutrients"]["PROCNT"]["quantity"], 2)
    }
    ingredients = recipe_data["ingredientLines"]
    recipe_url = recipe_data["url"]
    image_url = recipe_data["images"]["REGULAR"]["url"]
    time_to_cook = recipe_data["totalTime"]

    # Return the data without converting macros and ingredients to JSON strings
    return recipe_name, macros, ingredients, recipe_url, image_url, f"{time_to_cook} minutes", recipe_id, serving_size


# LANDING HOME PAGE
# DISPLAYS LANDING PAGE IF A USER IS NOT LOGGED IN 
# DISPLAYS SWIPE PAGE IF USER IS LOGGED IN
@bp.route('/')
def home_page():
    if 'user_id' in session:
        rName, rMacros, rIngredients, rURL, rIMG, rTime, rID, rServingSize = get_random_recipe()
        return render_template('main/index.html', image=rIMG, name=rName, time=rTime, macros=rMacros, ingredients=rIngredients, site = rURL)
    else:
        return render_template('landing/landing.html')

@bp.route('/contact')
def contact():
    return render_template('/landing/contact.html')

@bp.route('/about')
def about():
    return render_template('/landing/about.html')

@bp.route('/thankyou')
def thankYou():
    return render_template('/landing/thankYou.html')

@bp.route('/thankyou2')
def thankYou2():
    return render_template('/landing/thankYou2.html')

@bp.route('/landingtos')
def landingTOS():
    return render_template('/landing/landingTOS.html')

@bp.route('/landingpp')
def landingPP():
    return render_template('/landing/landingPP.html')

@bp.route('/onboarding')
@login_required
def onboarding():
    return render_template('/main/onboarding.html')

@bp.route('/saved')
@login_required
def saved():
    return render_template('/main/saved.html')

@bp.route('/tos')
@login_required
def tos():
    return render_template('/main/mainTOS.html')

@bp.route('/account')
@login_required
def account():
    return render_template('/main/account.html')

@bp.route('/privacypolicy')
@login_required
def privacypolicy():
    return render_template('/main/mainPP.html')


@bp.route('/findRecipes', methods=['GET', 'POST'])
@login_required
def query_user():
    try:
        if request.method == 'POST':
            cuisineType = request.form['cuisine']
            health = request.form['diet']
            mealType = request.form['meal_type']

        # Clear userParams from session
        session.pop('userParams', None)

        userParams = {'cuisineType': cuisineType, 'health': health, 'mealType': mealType}

        # If userParam value is empty, remove it from the dictionary
        userParams = {k: v for k, v in userParams.items() if v}

        session['userParams'] = userParams

        return render_template('main/recipequery.html')
    except Exception as e:
        print("An Exception Occured:", e)
        return "An error occured", 500

# Query of recipes
@bp.route('/findRecipes/search')
@login_required
def find_recipes():
    user_id = session['user_id']
    userParams = session.get('userParams', {})
    try:
        recipes = get_recipes(userParams, user_id)
    except Exception as error:
        # Out of recipes
        print("An Exception Occured:", error)
        recipes = None

    recipe_ids = [recipe.id for recipe in recipes]

    session['recipes_ids'] = recipe_ids
    if recipes == None:
        flash('No recipes found!')
    return render_template('main/recipes.html', recipes=recipes)

# Reveal more information (AJAX)
@bp.route('/findRecipes/<int:recipeID>/information')
def information(recipeID):
    user_id = session['user_id']
    error = None

    try:
        recipe = get_single_recipe_from_id(recipeID)
        recipeTaste = get_recipe_desc(recipe)
        recipeRecommendations = recommendation(user_id, recipeTaste, recipe)
    except Exception as e:
        error = str(e)

    if error is not None:
        return jsonify({'error': error}), 500

    # Construct the response data
    response_data = {
        'recipe': {
            'title': recipe.title,
            'image': recipe.image,
            'url': recipe.url,
            'totalTime': recipe.totalTime,
            'totalWeight': recipe.totalWeight,
            'calories': recipe.calories,
            'protein': recipe.protein,
            'carbs': recipe.carbs,
            'fat': recipe.fat,
            'sugar': recipe.sugar,
            'sodium': recipe.sodium
        },
        'recipeTaste': {
            'sweetness': recipeTaste.sweetness,
            'saltiness': recipeTaste.saltiness,
            'sourness': recipeTaste.sourness,
            'bitterness': recipeTaste.bitterness,
            'savoriness': recipeTaste.savoriness,
            'fattiness': recipeTaste.fattiness,
            'spiciness': recipeTaste.spiciness
        },
        'recipeRecommendations': {
            # Booleans for recommendations
            'sweetness': recipeRecommendations.sweetness,
            'saltiness': recipeRecommendations.saltiness,
            'sourness': recipeRecommendations.sourness,
            'bitterness': recipeRecommendations.bitterness,
            'savoriness': recipeRecommendations.savoriness,
            'fattiness': recipeRecommendations.fattiness,
            'spiciness': recipeRecommendations.spiciness,
            # Daily percent intake
            'calories': recipeRecommendations.calories,
            'protein': recipeRecommendations.protein,
            'carbs': recipeRecommendations.carbs,
            'fat': recipeRecommendations.fat,
            'sugar': recipeRecommendations.sugar,
            'sodium': recipeRecommendations.sodium
        }
    }

    return jsonify(response_data)

# TBA - Save recipe

# Update user preferences
@bp.route('/findRecipes/<int:recipeID>/<string:decision>')
def accept_reject_recipe(recipeID, decision):
    user_id = session['user_id']

    # Let string be "accept" or "reject"
    accept = True if decision == "accept" else False

    try:
        recipeTaste = get_recipedesc_from_id(recipeID)
        update_preferences(user_id, recipeTaste, accept)
    except Exception as e:
        error = str(e)

    # Return success
    return jsonify({'success': True})