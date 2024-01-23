from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from cookr.auth import login_required
from cookr.db import get_db

bp = Blueprint('index', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('main/index.html', posts=posts)

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