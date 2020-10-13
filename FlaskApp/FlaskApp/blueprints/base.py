from flask import Blueprint, render_template, flash, request, redirect, url_for, session, logging
from wtforms import Form, SelectField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.validators import DataRequired
import urllib.parse as up
import pandas as pd
import numpy as np
import sys

from FlaskApp import app, db #db is a mysql instance, shown in __init__.py

home_page = Blueprint('home_page', __name__,
                        template_folder='templates')

@home_page.route('/')
def index():
    return render_template('base/home.html')

about_page = Blueprint('about_page', __name__,
                        template_folder='templates')

@about_page.route('/about') #the url in the app.
def about():
    return render_template('base/about.html')
