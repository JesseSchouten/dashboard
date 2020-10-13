"""
Project folder structure according to the flask documentation for large application:
- https://flask.palletsprojects.com/en/1.1.x/patterns/packages/

Docstrings according to Restructured Text (;REST):
- Description: https://www.python.org/dev/peps/pep-0287/
- Examples: https://queirozf.com/entries/python-docstrings-reference-examples
"""

from flask import Flask
app = Flask(__name__)

#in development by default
from config import TestingConfig, DevelopmentConfig, ProductionConfig
app.config.from_object(DevelopmentConfig)

#Initialize database in
from flask_mysqldb import MySQL

# init MYSQL
db = MySQL()
db.init_app(app)

import FlaskApp.views
