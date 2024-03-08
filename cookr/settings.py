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
                insert_query = update_query = """
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
        except db.IntegrityError as e:
            error = f"Database Error: Couldn't {context} preferences for user {user_id} with the dietary options: {dietary_options}. Error: {e}"
            print(error)

        # Process the received data (for demonstration purposes, just echoing it back)
        return jsonify({"success": True, "message": "Dietary options received successfully", "data": dietary_options})

    except Exception as e:
        # Handle exceptions or errors
        return jsonify({"success": False, "message": str(e)})