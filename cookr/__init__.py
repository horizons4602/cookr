import os

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from cookr.scheduledjobs import recipe_ingredient_clean
import logging

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
        
    from . import auth
    app.register_blueprint(auth.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')
    
    create_scheduler(app)

    app.app_context().push()

    return app

def create_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Add scheduled jobs

    # Clean up old recipe records every 15 minutes
    scheduler.add_job(lambda: recipe_ingredient_clean(app), 'interval', minutes=1, id='clear_recipe_ingredient_records', misfire_grace_time=900)

    return scheduler