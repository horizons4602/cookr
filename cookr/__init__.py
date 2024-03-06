import os

from flask import Flask
from flask_apscheduler import APScheduler
from cookr.dbhelper import recipe_ingredient_clean
import logging

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Configure Flask logging
    app.logger.setLevel(logging.DEBUG)  # Set to ERROR in production
    scheduler = APScheduler()
    scheduler.init_app(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cookr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Cookr :)'
    
    from . import db
    db.init_app(app)

    # Delete expired recipes from "recipe" and "ingredient" tables
    # Every 12 minutes
    @scheduler.task('interval', id='clear_recipe_ingredient_records', minutes=15, misfire_grace_time=900)
    def clear_recipe_ingredient_records():
        try:
            recipe_ingredient_clean()
        except Exception as e:
            app.logger.error('An Exception Occured: %s', e)
            return "An error occured", 500
        
    from . import auth
    app.register_blueprint(auth.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    return app
