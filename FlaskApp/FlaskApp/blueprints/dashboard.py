from flask import Blueprint, render_template, flash, request, redirect, url_for, session, logging
from wtforms import Form, SelectField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.validators import DataRequired
import urllib.parse as up
import pandas as pd
import numpy as np
import sys
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show

from FlaskApp import app, db #db is a mysql instance, shown in __init__.py
from FlaskApp.blueprints.auth import login_required

dashboard_page = Blueprint('dashboard_page', __name__,
                        template_folder='templates')

@dashboard_page.route('/home_dashboard')
@login_required
def dashboard():
    #Create cursor
    cursor = db.connection.cursor()

    #Get articles
    if session['permissions'] == 'admin':
        result = cursor.execute("SELECT * FROM dashboard.articles;")
    else:
        result = cursor.execute("SELECT * FROM dashboard.articles WHERE author = %s", [session['username']])
    articles = cursor.fetchall()

    if result > 0:
        return render_template('dashboard/dashboard.html', articles=articles)
    else:
        return render_template('dashboard/dashboard.html')

def test_graph():
    x = [1, 3, 5, 7]
    y = [2, 4, 6, 8]

    p = figure(plot_width=300,plot_height=300)

    p.circle(x, y, size=10, color='red', legend_label='circle')
    p.line(x, y, color='blue', legend_label='line')
    p.triangle(y, x, color='gold', size=10, legend_label='triangle')
    p.legend.click_policy='hide'
    script, div = components(p)
    return script, div

dashboard_demo_page = Blueprint('dashboard_demo_page', __name__,
                        template_folder='templates')

@dashboard_demo_page.route('/dashboard_demo', methods=['GET', 'POST'])
@login_required
def dashboard_demo():
    script_test_graph, div_test_graph = test_graph()

    if session['permissions'] == 'admin' or session['permissions'] == 'developer':
        return render_template(
        'dashboard/dashboard_demo.html',
        div_test_graph=div_test_graph,
        script_test_graph=script_test_graph
        )
    else:
        flash('Permission Denied', 'danger')
        return render_template('dashboard/dashboard.html')
