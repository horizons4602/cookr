# Service for clearing records from the database, functions for common database uses

from cookr.db import get_db
from datetime import datetime, timedelta
from cookr.edamamrecipeapi import Recipe

# Delete expired recipes from "recipe" and "ingredient" tables

# Get current time and date, formatted for DATETIME type
def recipe_ingredient_clean():
    current_datetime = datetime.now()
    fifteen_minutes_ago = (current_datetime - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
    db = get_db()
    
    # Get expired recipe records
    expired_query = db.execute("SELECT * FROM recipe WHERE creationTime >= ?", (fifteen_minutes_ago,))

    recipes = expired_query.fetchall()

    # Delete expired recipe and ingredient records
    for recipe in recipes:
        db.execute("DELETE FROM ingredient WHERE recipe_id = ?", (recipe['id']))
        db.execute("DELETE FROM recipe WHERE recipe_id = ?", (recipe['id']))

    db.commit()

def get_recipes_from_ids(recipe_ids):
    db = get_db()

    # Get the recipes from the database using the recipe IDs
    placeholders = ', '.join('?' for _ in recipe_ids)
    query = f'SELECT * FROM recipe WHERE id IN ({placeholders})'
    recipes_queries = db.execute(query, recipe_ids).fetchall()

    # Create Recipe objects from the database query
    recipes = []

    for recipe_id in recipe_ids:
        recipe = recipes_queries[recipe_id]
        ingredients_query = db.execute('SELECT * FROM ingredient WHERE recipe_id = ?', (recipe_id,)).fetchall()
        ingredients = [ingredient['name'] for ingredient in ingredients_query]
        recipe = Recipe(recipe['id'], recipe['selfHref'], recipe['image'], recipe['url'], recipe['title'], ingredients, recipe['calories'], recipe['totalWeight'], recipe['totalTime'])
        recipes.append(recipe)
    
    return recipes

def get_single_recipe_from_id(recipe_id):
    db = get_db()

    # Get the recipe from the database using the recipe ID
    recipe_query = db.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,)).fetchone()
    ingredients_query = db.execute('SELECT * FROM ingredient WHERE recipe_id = ?', (recipe_id,)).fetchall()
    ingredients = [ingredient['name'] for ingredient in ingredients_query]
    recipe = Recipe(recipe_query['id'], recipe_query['selfHref'], recipe_query['image'], recipe_query['url'], recipe_query['title'], ingredients, recipe_query['calories'], recipe_query['totalWeight'], recipe_query['totalTime'])