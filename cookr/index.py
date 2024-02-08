from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
import logging

from cookr.auth import login_required
from cookr.db import get_db
from cookr.recipeapi import get_recipes, get_recipe_desc

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def home_page():
    #session.clear()
    return render_template('main/index.html')

@bp.route('/findRecipes', methods=['GET', 'POST'])
@login_required
def query_user():
    if request.method == 'POST':
        cuisineType = request.form['cuisine']
        health = request.form['diet']
        mealType = request.form['meal_type']

        session['cuisineType'] = cuisineType
        session['health'] = health
        session['mealType'] = mealType
        return redirect(url_for('index.find_recipes', offset=0))
    return render_template('main/recipequery.html')

@bp.route('/findRecipes/<int:offset>')
@login_required
def find_recipes(offset):
    userParams = {'cuisine': session.get('cuisineType'), 'diet': session.get('health'), 'type': session.get('mealType'), 'offset': offset}
    
    # Remove empty values from userParams
    userParams = {k: v for k, v in userParams.items() if v}
    
    recipes = get_recipes(userParams)
    if recipes == "No Recipes Found":
        flash('No results found!')
    if recipes == "Out of Recipes":
        flash('No more results found!')
    if recipes == "Out of API Calls":
        flash('Service Temporarily Down, Please Try Again Later')
    return render_template('main/recipes.html', recipes=recipes, params=userParams)

# Accept or Reject recipe route
bp.route('/swipe/<action>/<int:recipe_id>')
def swipe(action, recipe_id):
    # Add logic here to handle user's swipe (accept or reject)
    # We'll make a preferences algorithm that's pretty good, neat, complicated so we can show off to Dr. Shin
    # Only acquire more info when the user views more about the recipe (due to limits :)
    # For now, we'll just redirect to the home page
    return redirect(url_for('index'))

# Generate new recipes route
@bp.route('/generate')
def generate():
    offset = session.get('offset', 0)
    offset += 20
    session['offset'] = offset
    return redirect(url_for('index'))

# Generate new recipes route
@bp.route('/recipeTaste/<int:recipe_id>')
def recipe_information(recipe_id):
    get_recipe_desc(recipe_id)

@bp.route('/saved')
@login_required
def saved():
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