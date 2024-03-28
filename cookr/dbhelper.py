# Service for clearing records from the database, functions for common database uses

from cookr.db import get_db
from cookr.recipeclasses import Recipe, RecipeDesc
from datetime import datetime

def insert_recipe_cache(recipe: Recipe, user_id):
    # Get current time and date, formatted for DATETIME type
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()

    context = "Recipe Database"

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO recipe (creationTime, selfHref, image, url, title, calories, totalWeight, totalTime, protein, carbs, fat, sugar, sodium, saving_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (current_datetime, recipe.selfHref, recipe.image, recipe.url, recipe.title, recipe.calories, recipe.totalWeight, recipe.totalTime, recipe.protein, recipe.carbs, recipe.fat, recipe.sugar, recipe.sodium, user_id),
        )

        # Get the last inserted row's id
        recipe_id = cursor.lastrowid

        # Database ID for recipe object
        id = recipe_id

        context = "Ingredient Database"

        for ingredient in recipe.ingredients:
            cursor.execute(
                "INSERT INTO ingredient (recipe_ID, name) VALUES (?, ?)",
                (recipe_id, ingredient),
            )
        
        db.commit()

        return id
        
    except db.IntegrityError:
        # Should not occur, but just in case ¯\_(ツ)_/¯ 
        error = f"Database {context} Error: Recipe {recipe} could not be inserted into Database."
        print(error)

# Refresh time for deletion by scheduler; for when recipe taste info is queried
def refresh_recipe_cache(recipe_id):
    # Get current time and date, formatted for DATETIME type
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()

    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE recipe SET creationTime = ? WHERE id = ?",
            (current_datetime, recipe_id),
        )
        
        db.commit()
        
    except db.IntegrityError:
        # Should not occur, but just in case ¯\_(ツ)_/¯ 
        error = f"Database recipe error: Recipe {recipe_id} could not be updated with a refreshed timer in the Database."
        print(error)

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
        recipe = Recipe(recipe['id'], recipe['selfHref'], recipe['image'], recipe['url'], recipe['title'], ingredients, recipe['calories'], recipe['totalWeight'], recipe['totalTime'], recipe['protein'], recipe['carbs'], recipe['fat'], recipe['sugar'], recipe['sodium'])
        recipes.append(recipe)
    
    return recipes

def get_single_recipe_from_id(recipe_id):
    db = get_db()

    # Get the recipe from the database using the recipe ID
    try:
        recipe_query = db.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,)).fetchone()
        ingredients_query = db.execute('SELECT * FROM ingredient WHERE recipe_id = ?', (recipe_id,)).fetchall()
    except:
        raise Exception(f"Database Error: Recipe with ID {recipe_id} could not be found. Likely expired.")
    ingredients = [ingredient['name'] for ingredient in ingredients_query]
    recipe = Recipe(recipe_query['id'], recipe_query['selfHref'], recipe_query['image'], recipe_query['url'], recipe_query['title'], ingredients, recipe_query['calories'], recipe_query['totalWeight'], recipe_query['totalTime'], recipe_query['protein'], recipe_query['carbs'], recipe_query['fat'], recipe_query['sugar'], recipe_query['sodium'])

    return recipe

def get_user_health_restrictions(user_id):
    db = get_db()

    user_diet_info = db.execute('SELECT * FROM user_health WHERE saving_user = ?', (user_id,)).fetchone()

    cursor = db.execute('SELECT * FROM user_health WHERE saving_user = ?', (user_id,))

    attributes = [description[0] for description in cursor.description]

    user_health = {}

    if user_diet_info:
        for attribute, boolValue in zip(attributes, user_diet_info):   
            if attribute != "saving_user":
                user_health[attribute] = boolValue
    else: 
        user_health = {attribute: False for attribute in attributes if attribute != "saving_user"}

    return user_health

def get_user_preferences(user_id):
    db = get_db()

    try:
        preferences = db.execute('SELECT * FROM user_preference WHERE saving_user = ?', (user_id,)).fetchone()
    except:
        raise Exception(f"Database Error: User preferences with ID {user_id} query could not be executed.")

    return RecipeDesc(preferences['sweetness'], preferences['saltiness'], preferences['sourness'], preferences['bitterness'], preferences['savoriness'], preferences['fattiness'], preferences['spiciness'])

def initialize_user_preferences(user_id):
    _default = 50

    db = get_db()

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user_preference (saving_user, sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, _default, _default, _default, _default, _default, _default, _default),
        )
        db.commit()
    except db.IntegrityError:
        error = f"Database Error: User preferences with ID {user_id} could not be inserted into Database."
        print(error)

def update_user_preferences(user_id, preferences: RecipeDesc):
    db = get_db()

    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE user_preference SET sweetness = ?, saltiness = ?, sourness = ?, bitterness = ?, savoriness = ?, fattiness = ?, spiciness = ? WHERE saving_user = ?",
            (preferences.sweetness, preferences.saltiness, preferences.sourness, preferences.bitterness, preferences.savoriness, preferences.fattiness, preferences.spiciness, user_id),
        )
        db.commit()
    except db.Error:
        error = f"Database Error: User preferences with ID {user_id} could not be updated in Database."
        print(error)

    exists = db.execute('SELECT * FROM user_preference WHERE saving_user = ?', (user_id,)).fetchone()

    if exists is None:
        initialize_user_preferences(user_id)

def get_user_macronutrients(user_id):
    db = get_db()

    try:
        macronutrients = db.execute('SELECT * FROM macro_info WHERE saving_user = ?', (user_id,)).fetchone()
    except:
        raise Exception(f"Database Error: User macronutrients with ID {user_id} query could not be executed.")

    if macronutrients is None:
        return macronutrients

    return macronutrients

def insert_recipedesc_cache(recipedesc: RecipeDesc, recipe_id):
    db = get_db()

    try:

        try:
            refresh_recipe_cache(recipe_id)
        except:
            raise Exception(f"Database Error: Recipe with ID {recipe_id} could not be found. Likely expired.")
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO recipe_taste (sweetness, saltiness, sourness, bitterness, savoriness, fattiness, spiciness, recipe_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (recipedesc.sweetness, recipedesc.saltiness, recipedesc.sourness, recipedesc.bitterness, recipedesc.savoriness, recipedesc.fattiness, recipedesc.spiciness, recipe_id),
        )
        db.commit()
    except db.IntegrityError:
        error = f"Database Error: Recipe taste description for recipe ID {recipe_id} could not be inserted into Database."
        print(error)

def get_recipedesc_from_id(recipe_id):
    db = get_db()

    try:
        recipedesc = db.execute('SELECT * FROM recipe_taste WHERE recipe_id = ?', (recipe_id,)).fetchone()
    except:
        raise Exception(f"Database Error: Recipe taste description with ID {recipe_id} query could not be executed.")

    return RecipeDesc(recipedesc['sweetness'], recipedesc['saltiness'], recipedesc['sourness'], recipedesc['bitterness'], recipedesc['savoriness'], recipedesc['fattiness'], recipedesc['spiciness'])

def insert_saved_recipe(user_id, recipe_id):
    # Get current time and date, formatted for DATETIME type
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()

    recipe = get_single_recipe_from_id(recipe_id)

    try:
        cursor = db.cursor()

        # Check the number of saved recipes for the user
        cursor.execute("SELECT COUNT(*) FROM saved_recipe WHERE saving_user = ?", (user_id,))
        num_saved_recipes = cursor.fetchone()[0]

        if num_saved_recipes >= 6:
            # Delete the oldest recipe (replace)
            cursor.execute("DELETE FROM saved_recipe WHERE saving_user = ? ORDER BY creationTime ASC LIMIT 1", (user_id,))
            print(f"Oldest recipe replaced for user {user_id}.")

        # Insert the new recipe
        cursor.execute(
            "INSERT INTO saved_recipe (title, creationTime, url, calories, totalWeight, totalTime, protein, carbs, fat, sugar, sodium, saving_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (recipe.title, current_datetime, recipe.url, recipe.calories, recipe.totalWeight, recipe.totalTime, recipe.protein, recipe.carbs, recipe.fat, recipe.sugar, recipe.sodium, user_id),
        )
        db.commit()
    except db.IntegrityError:
        error = f"Database Error: Recipe with ID {recipe_id} could not be saved for user {user_id}."
        print(error)


def get_saved_recipes(user_id):
    db = get_db()

    recipes = []

    try:
        saved_recipes = db.execute('SELECT * FROM saved_recipe WHERE saving_user = ?', (user_id,)).fetchall()

        for saved_recipe in saved_recipes:
            # Recipe not total, only specific fields
            recipe = Recipe(None, None, None, saved_recipe['url'], saved_recipe['title'], None, saved_recipe['calories'], saved_recipe['totalWeight'], saved_recipe['totalTime'], saved_recipe['protein'], saved_recipe['carbs'], saved_recipe['fat'], saved_recipe['sugar'], saved_recipe['sodium'])
            recipes.append(recipe)
    except:
        raise Exception(f"Database Error: Saved recipes with ID {user_id} query could not be executed.")

    return saved_recipes