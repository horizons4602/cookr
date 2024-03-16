from flask import (
<<<<<<< HEAD
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
=======
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify, logging
>>>>>>> 7e05f652284689404d4c652a5dd2891d700396f1
)
from werkzeug.exceptions import abort

from cookr.auth import login_required
from cookr.db import get_db
from cookr.dbhelper import get_recipes_from_ids, get_single_recipe_from_id, get_recipedesc_from_id
from cookr.edamamrecipeapi import get_recipes
from cookr.recipeapi import get_recipe_desc
from cookr.recipeclasses import Recipe, RecipeRecommendation
from cookr.preference import update_preferences, recommendation

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def home_page():
    try:
        #session.clear()
        return render_template('main/index.html')
    except Exception as e:
        print("An Exception Occured:", e)
        return "An error occured", 500

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
    
@bp.route('/saved')
@login_required
def saved():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10

        db = get_db()
        
        # Check if the random recipe list is already in the session
        if 'random_recipe_ids' not in session:
            # Fetch a random set of recipe IDs
            random_recipe_ids = db.execute(
                'SELECT id FROM recipe ORDER BY RANDOM() LIMIT ?',
                (per_page,)
            ).fetchall()

            # Store the list in the session
            session['random_recipe_ids'] = [row['id'] for row in random_recipe_ids]

        # Get the appropriate subset of recipe IDs based on the current page
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        current_recipe_ids = session['random_recipe_ids'][start_index:end_index]

        # Fetch the details of the recipes
        savedRecipes = db.execute(
            'SELECT r.id, title, image, imageType, saving_user'
            ' FROM recipe r JOIN user u ON r.saving_user = u.id'
            ' WHERE r.id IN ({})'.format(','.join(map(str, current_recipe_ids)))
        ).fetchall()

<<<<<<< HEAD
        # Store the list in the session
        session['random_recipe_ids'] = [row['id'] for row in random_recipe_ids]

    # Get the appropriate subset of recipe IDs based on the current page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    current_recipe_ids = session['random_recipe_ids'][start_index:end_index]

    # Fetch the details of the recipes
    savedRecipes = db.execute(
        'SELECT r.id, title, image, imageType, saving_user'
        ' FROM recipe r JOIN user u ON r.saving_user = u.id'
        ' WHERE r.id IN ({})'.format(','.join(map(str, current_recipe_ids)))
    ).fetchall()

    return render_template('main/saved.html', recipes=savedRecipes, page=page)
=======
        return render_template('main/saved.html', recipes=savedRecipes, page=page)
    except Exception as e:
        print("An Exception Occured:", e)
        return "An error occured", 500
>>>>>>> 7e05f652284689404d4c652a5dd2891d700396f1
