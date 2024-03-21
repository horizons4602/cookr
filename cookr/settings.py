from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort

from cookr.db import get_db
from cookr.dbhelper import get_user_health_restrictions
from cookr.auth import login_required

bp = Blueprint('settings', __name__, url_prefix='/settings')

@bp.route('/dietRestrictions')
@login_required
def dietsettings():
    user_id = session['user_id']
    
    user_health = get_user_health_restrictions(user_id)

    return render_template('settings/diet.html', diet=user_health)

@bp.route('/dietMacronutrients', methods=('GET', 'POST'))
@login_required
def macros():
    user_id = session['user_id']

    if request.method == 'POST':
        # Get user information from the form (Validate info immediately)
        user_weight = float(request.form['userWeight']) # Must be in lbs
        user_height = float(request.form['userHeight']) # Must be in inches
        user_age = int(request.form['userAge']) # Must be in years
        user_sex = request.form['userSex'] # Male/Female
        user_activity_level = float(request.form['userActivityLevel']) # Predetermined values specified on the HTML

        try:
            calories = calculate_calories(user_weight, user_height, user_age, user_sex, user_activity_level)
        except Exception as e:
            error = f"Error calculating calories: {e}"

        user_protein = calories / 4
        user_carbs = calories / 4
        user_fat = calories / 9
        user_sugar = 36.0 if user_sex == "Male" else 25.0 # Added sugar limit in grams
        user_sodium = 2300.0

        error = None
        
        if not user_weight:
            error = 'userWeight is required.'
        elif not user_sex:
            error = 'Sex is required.'
        elif not user_height:
            error = 'Height is required'
        elif not user_age:
            error = 'Age is required'
        elif not user_activity_level:
            error = 'Activity level is required'

        db = get_db()

        if error is None:
            try:
                context = "update"
                update_query = """
                    UPDATE macro_info
                    SET 
                        user_weight = ?,
                        user_sex = ?,
                        user_height = ?,
                        user_age = ?,
                        user_activity_level = ?,
                        user_calories = ?,
                        user_protein = ?,
                        user_carbs = ?,
                        user_fat = ?,
                        user_sugar = ?,
                        user_sodium = ?
                    WHERE saving_user = ?
                """

                update = db.execute(update_query, (
                    user_weight, user_sex, user_height, user_age, user_activity_level, calories, user_protein, user_carbs, user_fat, user_sugar, user_sodium, user_id
                ))
                
                user_diet_info = db.execute('SELECT * FROM macro_info WHERE saving_user = ?', (user_id,)).fetchone()

                if user_diet_info is None:
                    insert_query = """
                        INSERT INTO macro_info 
                        (user_weight, user_sex, user_height, user_age, user_activity_level, user_calories, 
                        user_protein, user_carbs, user_fat, user_sugar, user_sodium, saving_user) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """

                    db.execute(
                        insert_query,
                        (user_weight, user_sex, user_height, user_age, user_activity_level, calories, user_protein, user_carbs, user_fat, user_sugar, user_sodium, user_id)
                    ).fetchone()

                db.commit()
            except db.Error as e:
                error = f"""Database Error: Couldn't {context} preferences for user {user_id} with the macronutrient options:
                user_weight: {user_weight}, user_sex: {user_sex}, user_height: {user_height}, user_age: {user_age}, user_activity_level: {user_activity_level}. 
                Error: {e}"""
                print(error)
                flash("Sorry, there was an error updating your macronutrient preferences.")
        else: 
            flash("Sorry, there was an error updating your macronutrient preferences.")

    return render_template('settings/nutrition.html')

@bp.route('/submitDietaryOptions', methods = ['POST'])
def dietsettingssubmit():
    user_id = session['user_id']

    try:
        # Get the JSON data from the request
        dietary_options = request.get_json()

        alcohol_cocktail = dietary_options.get("alcohol_cocktail")
        alcohol_free = dietary_options.get("alcohol_free")
        celery_free = dietary_options.get("celery_free")
        crustacean_free = dietary_options.get("crustacean_free")
        dairy_free = dietary_options.get("dairy_free")
        dash = dietary_options.get("dash")
        egg_free = dietary_options.get("egg_free")
        fish_free = dietary_options.get("fish_free")
        fodmap_free = dietary_options.get("fodmap_free")
        gluten_free = dietary_options.get("gluten_free")
        immuno_supportive = dietary_options.get("immuno_supportive")
        keto_friendly = dietary_options.get("keto_friendly")
        kidney_friendly = dietary_options.get("kidney_friendly")
        kosher = dietary_options.get("kosher")
        low_fat_abs = dietary_options.get("low_fat_abs")
        low_potassium = dietary_options.get("low_potassium")
        low_sugar = dietary_options.get("low_sugar")
        lupine_free = dietary_options.get("lupine_free")
        Mediterranean = dietary_options.get("Mediterranean")
        mollusk_free = dietary_options.get("mollusk_free")
        mustard_free = dietary_options.get("mustard_free")
        no_oil_added = dietary_options.get("no_oil_added")
        paleo = dietary_options.get("paleo")
        peanut_free = dietary_options.get("peanut_free")
        pescatarian = dietary_options.get("pescatarian")
        pork_free = dietary_options.get("pork_free")
        red_meat_free = dietary_options.get("red_meat_free")
        sesame_free = dietary_options.get("sesame_free")
        shellfish_free = dietary_options.get("shellfish_free")
        soy_free = dietary_options.get("soy_free")
        sugar_conscious = dietary_options.get("sugar_conscious")
        sulfite_free = dietary_options.get("sulfite_free")
        tree_nut_free = dietary_options.get("tree_nut_free")
        vegan = dietary_options.get("vegan")
        vegetarian = dietary_options.get("vegetarian")
        wheat_free = dietary_options.get("wheat_free")

        db = get_db()

        # Update the user's dietary restrictions
        try:
            context = "update"
            update_query = """
                UPDATE user_health 
                SET 
                    alcohol_cocktail = ?, alcohol_free = ?, celery_free = ?, crustacean_free = ?, dairy_free = ?, 
                    dash = ?, egg_free = ?, fish_free = ?, fodmap_free = ?, gluten_free = ?, immuno_supportive = ?, 
                    keto_friendly = ?, kidney_friendly = ?, kosher = ?, low_fat_abs = ?, low_potassium = ?, low_sugar = ?, 
                    lupine_free = ?, Mediterranean = ?, mollusk_free = ?, mustard_free = ?, no_oil_added = ?, paleo = ?, 
                    peanut_free = ?, pescatarian = ?, pork_free = ?, red_meat_free = ?, sesame_free = ?, shellfish_free = ?, 
                    soy_free = ?, sugar_conscious = ?, sulfite_free = ?, tree_nut_free = ?, vegan = ?, vegetarian = ?, 
                    wheat_free = ?
                WHERE saving_user = ?
            """

            update = db.execute(update_query, (
                alcohol_cocktail, alcohol_free, celery_free, crustacean_free, dairy_free, 
                dash, egg_free, fish_free, fodmap_free, gluten_free, immuno_supportive, 
                keto_friendly, kidney_friendly, kosher, low_fat_abs, low_potassium, low_sugar, 
                lupine_free, Mediterranean, mollusk_free, mustard_free, no_oil_added, paleo, 
                peanut_free, pescatarian, pork_free, red_meat_free, sesame_free, shellfish_free, 
                soy_free, sugar_conscious, sulfite_free, tree_nut_free, vegan, vegetarian, wheat_free,
                user_id
            ))
            
            user_diet_info = db.execute('SELECT * FROM user_health WHERE saving_user = ?', (user_id,)).fetchone()

            if user_diet_info is None:
                context = "insert"
                insert_query = """
                    INSERT INTO user_health (saving_user, alcohol_cocktail, alcohol_free, celery_free, crustacean_free, dairy_free, 
                    dash, egg_free, fish_free, fodmap_free, gluten_free, immuno_supportive, keto_friendly, kidney_friendly, kosher,
                    low_fat_abs, low_potassium, low_sugar, lupine_free, Mediterranean, mollusk_free, mustard_free, no_oil_added,
                    paleo, peanut_free, pescatarian, pork_free, red_meat_free, sesame_free, shellfish_free, soy_free, sugar_conscious,
                    sulfite_free, tree_nut_free, vegan, vegetarian, wheat_free) 
                    VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                db.execute(insert_query, (
                    alcohol_cocktail, alcohol_free, celery_free, crustacean_free, dairy_free, 
                    dash, egg_free, fish_free, fodmap_free, gluten_free, immuno_supportive, 
                    keto_friendly, kidney_friendly, kosher, low_fat_abs, low_potassium, low_sugar, 
                    lupine_free, Mediterranean, mollusk_free, mustard_free, no_oil_added, paleo, 
                    peanut_free, pescatarian, pork_free, red_meat_free, sesame_free, shellfish_free, 
                    soy_free, sugar_conscious, sulfite_free, tree_nut_free, vegan, vegetarian, wheat_free,
                    user_id
                ))

            db.commit()
        except db.Error as e:
            error = f"Database Error: Couldn't {context} preferences for user {user_id} with the dietary options: {dietary_options}. Error: {e}"
            print(error)

        # Process the received data (for demonstration purposes, just echoing it back)
        return jsonify({"success": True, "message": "Dietary options received successfully", "data": dietary_options})

    except Exception as e:
        # Handle exceptions or errors
        return jsonify({"success": False, "message": str(e)})
    
def calculate_calories(weight, height, age, sex, activity_level):
    """
    Calculate daily calorie needs based on user information.

    Parameters:
    - weight: User's weight in kilograms
    - height: User's height in centimeters
    - age: User's age in years
    - sex: User's sex (either 'Male' or 'Female')
    - activity_level: User's activity level (a float value)

    Returns:
    - Calories: Daily calorie needs based on the Harris-Benedict equation
    """
    if sex == "Male":
        calories = (66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)) * activity_level
    else:
        calories = (655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)) * activity_level
    return calories