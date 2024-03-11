"""
Title: app.py
Author: Noah Fry, Brady Spencer, Maximus Meadowcroft, Jason Kern
Brief: Provides wep app functionality for the cookr website and kitchen aid
"""
from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login')
def login(): 
    return 'Login'

@app.route('/about')
def about():
    return 'About'

@app.route('/contact')
def contact():
    return 'Contact'

@app.route('/recipes')
def recipes():
    return 'Recipes'

@app.route('/settings')
def settings():
    return 'Settings'

if __name__ == '__main__':
    app.run(debug = True)