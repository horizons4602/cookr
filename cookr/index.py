from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify, logging
)
from werkzeug.exceptions import abort

from cookr.auth import login_required
from cookr.db import get_db
from cookr.dbhelper import get_recipes_from_ids, get_single_recipe_from_id
from cookr.edamamrecipeapi import get_recipes
from cookr.recipeapi import get_recipe_desc

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
            session.pop('next', None)

            userParams = {'cuisineType': cuisineType, 'health': health, 'mealType': mealType}

            # If userParam value is empty, remove it from the dictionary
            userParams = {k: v for k, v in userParams.items() if v}

            session['userParams'] = userParams

            return redirect(url_for('index.find_recipes'))
        return render_template('main/recipequery.html')
    except Exception as e:
        print("An Exception Occured:", e)
        return "An error occured", 500

# Initial query of recipes, future queries will be handled by the generate route (if more recipes exist)
@bp.route('/findRecipes/search')
@login_required
def find_recipes():
    user_id = session['user_id']
    userParams = session.get('userParams', {})
    try:
        recipes, next = get_recipes(userParams, None, user_id)
    except Exception as error:
        # Out of recipes
        print("An Exception Occured:", error)
        recipes = None
        next = None

    recipe_ids = [recipe.id for recipe in recipes]

    session['recipes_ids'] = recipe_ids
    session['next'] = next
    if recipes == None:
        flash('No recipes found!')
    return render_template('main/recipes.html', recipes=recipes)

# Reveal more information (to be called dynamically)
@bp.route('/findRecipes/<int:recipeID>/information')
def information(recipeID):
    try:
        # Get the recipe information
        recipe = get_single_recipe_from_id(recipeID)
        recipeTaste = get_recipe_desc(recipe)

        # COMPARE TASTE TO USER PREFERENCE HERE, TBD

        # For AJAX requests
        # Return JSON
        return jsonify({
            'recipe': {
                'title': recipe.title,
                'image': recipe.image,
                'url': recipe.url,
                # Add more fields as needed
            },
            'recipeTaste': {
                'sweetness': recipeTaste.sweetness,
                'saltiness': recipeTaste.saltiness,
                'sourness': recipeTaste.sourness,
                'bitterness': recipeTaste.bitterness,
                'savoriness': recipeTaste.savoriness,
                'fattiness': recipeTaste.fattiness,
                'spiciness': recipeTaste.spiciness,
            },
            # Likely more fields for comparison to user tastes here (booleans)
        })
    except Exception as e:
        print("An Exception Occured:", e)
        return "An error occured", 500

# Generate new recipes route
@bp.route('/findRecipes/generate')
def generate():
    user_id = session['user_id']
    next = session['next']
    try:
        recipes, next = get_recipes(None, next, user_id)
        session['next'] = next

        # Store recipe.title
        recipe_ids = [recipe.id for recipe in recipes]
        
        session['recipes_ids'] = recipe_ids
    except:
        # Out of recipes
        recipes = None
        next = None
    return render_template('main/recipes.html', recipes=recipes)

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

        return render_template('main/saved.html', recipes=savedRecipes, page=page)
    except Exception as e:
        print("An Exception Occured:", e)
        return "An error occured", 500