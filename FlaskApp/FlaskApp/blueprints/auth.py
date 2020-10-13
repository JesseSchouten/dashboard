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
from FlaskApp.blueprints.base import home_page

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match!'),
    ])
    confirm = PasswordField('Confirm Password')

#User registry
register_page = Blueprint('register_page', __name__,
                        template_folder='templates')

@register_page.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(str(form.password.data))

        #create cursor
        cur = db.connection.cursor()
        try:
            cur.execute("INSERT INTO dashboard.users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username,(password)))
        except Exception as e:
            if type(e).__name__ == 'IntegrityError':
                flash('This username already exists!', 'danger')
                return render_template('auth/register.html', form=form)
            else:
                flash('An unknown error occurred, try again!', 'danger')
                return render_template('auth/register.html', form=form)
        #commit to db
        db.connection.commit()

        #close connection
        cur.close()

        flash('You are now registered and can log in.','success')

        return redirect(url_for('home_page.index'))
    return render_template('auth/register.html', form=form)

#User login
login_page = Blueprint('login_page', __name__,
                        template_folder='templates')

@login_page.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Create cursor
        cursor = db.connection.cursor()

        #Get user by Username
        result = cursor.execute("SELECT * FROM dashboard.users WHERE BINARY username = %s", [username])

        if result > 0:
            #Get stored hash
            data = cursor.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['permissions'] = data['permissions']
                if data['permissions'] == 'admin':
                    session['admin_permissions'] = True

                flash('You are now logged in.', 'success')
                return redirect(url_for('home_page.index'))
            else:
                error = "Invalid login"
                return render_template('auth/login.html', error=error)
            #Close connection
            cursor.close()
        else:
            error = "Username not found."
            return render_template('auth/login.html', error=error)

    return render_template('auth/login.html')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login.', 'danger')
            return redirect(url_for('home_page.index'))
    return wrap

#logout
logout_page = Blueprint('logout_page', __name__,
                        template_folder='templates')
@logout_page.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login_page.login'))
