from cookr.db import get_db
from cookr.recipeclasses import Recipe, RecipeDesc
from datetime import datetime, timedelta

# Delete recipes with a creation time of over 15 minutes ago
def recipe_ingredient_clean(app):
    with app.app_context():
        current_datetime = datetime.now()
        fifteen_minutes_ago = (current_datetime - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
        db = get_db()
        
        # Get expired recipe records
        expired_query = db.execute("SELECT * FROM recipe WHERE creationTime < ?", (fifteen_minutes_ago,))
    
        recipes = expired_query.fetchall()
    
        # Delete expired recipe and ingredient records
        for recipe in recipes:
            db.execute("DELETE FROM ingredient WHERE recipe_id = ?", (recipe['id'],))
            db.execute("DELETE FROM recipe WHERE id = ?", (recipe['id'],))
    
        db.commit()