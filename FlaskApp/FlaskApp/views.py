from FlaskApp import app
from flask import Blueprint, render_template, flash, request, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, SelectField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from wtforms.validators import DataRequired
import urllib.parse as up
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
import numpy as np
import sys
from config import Config, TestingConfig, DevelopmentConfig, ProductionConfig

app.config.from_object("DevelopmentConfig")

# init MYSQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about') #the url in the app.
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(str(form.password.data))

        #create cursor
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO dashboard.users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username,(password)))
        except Exception as e:
            if type(e).__name__ == 'IntegrityError':
                flash('This username already exists!', 'danger')
                return render_template('register.html', form=form)
            else:
                flash('An unknown error occurred, try again!', 'danger')
                return render_template('register.html', form=form)
        #commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('You are now registered and can log in.','success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)

#User login
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Create cursor
        cursor = mysql.connection.cursor()

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
                return redirect(url_for('index'))
            else:
                error = "Invalid login"
                return render_template('login.html', error=error)
            #Close connection
            cursor.close()
        else:
            error = "Username not found."
            return render_template('login.html', error=error)

    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login.', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/articles') #the url in the app.
@login_required
def articles():
    #Create cursor
    cursor = mysql.connection.cursor()

    #Get articles
    result = cursor.execute("SELECT * FROM dashboard.articles")

    articles = cursor.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        return render_template('articles.html')

@app.route('/article/<string:id>') #the url in the app.
@login_required
def article(id):
    cursor = mysql.connection.cursor()

    #Get articles
    result = cursor.execute("SELECT * FROM dashboard.articles WHERE id = %s", [id])
    article = cursor.fetchone()

    return render_template('article.html', article=article)

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match!'),
    ])
    confirm = PasswordField('Confirm Password')

#logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/home_dashboard')
@login_required
def dashboard():
    #Create cursor
    cursor = mysql.connection.cursor()

    #Get articles
    if session['permissions'] == 'admin':
        result = cursor.execute("SELECT * FROM dashboard.articles;")
    else:
        result = cursor.execute("SELECT * FROM dashboard.articles WHERE author = %s", [session['username']])
    articles = cursor.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        return render_template('dashboard.html')

#Article Form Class
class ArticleForm(Form):
    title = StringField('Name',[validators.Length(min=1, max=200)])
    body = TextAreaField('Text',[validators.Length(min=30)])

@app.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        #Create DictCursor
        cursor = mysql.connection.cursor()

        #Execute
        cursor.execute("INSERT INTO dashboard.articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        #Commit
        mysql.connection.commit()

        #Close connection
        cursor.close()

        flash('Documentation Created', 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    #Create cursor
    cursor = mysql.connection.cursor()

    #Get article by id
    result = cursor.execute("SELECT * FROM dashboard.articles WHERE id=%s", [id])

    article = cursor.fetchone()

    #Get form
    form = ArticleForm(request.form)

    #Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        #Create DictCursor
        cursor = mysql.connection.cursor()

        #Execute
        cursor.execute("UPDATE dashboard.articles SET title = %s, body = %s, updated=CURRENT_TIMESTAMP() WHERE id = %s", (title, body, id))

        #Commit
        mysql.connection.commit()

        #Close connection
        cursor.close()

        flash('Documentation Updated', 'success')

        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)

#Delete article
@app.route('/delete_article/<string:id>', methods=['POST'])
@login_required
def delete_article(id):
    #Create cursor
    cursor = mysql.connection.cursor()

    #Execute
    cursor.execute("DELETE FROM dashboard.articles WHERE id = %s", [id])

    #Commit
    mysql.connection.commit()

    #Close connection
    cursor.close()

    flash('Documentation Deleted', 'success')

    return redirect(url_for('dashboard'))

@app.route('/admin_page')
@login_required
def admin_page():
    #Create cursor
    cursor = mysql.connection.cursor()

    #Get articles
    result = cursor.execute("SELECT id, name, email, username, permissions FROM dashboard.users;")

    users = cursor.fetchall()

    if result > 0:
        return render_template('admin_page.html', users=users)
    else:
        return render_template('admin_page.html')

@app.route('/update_permissions/<string:username>_<string:new_permissions>', methods=['POST'])
@login_required
def update_permissions(username, new_permissions):
    #Create cursor
    cursor = mysql.connection.cursor()

    #Execute
    if username == session['username']:
        flash("We can't update our own permissions!", 'danger')
        return redirect(url_for('admin_page'))
    cursor.execute("UPDATE dashboard.users SET permissions= %s, updated = CURRENT_TIMESTAMP() WHERE username = %s;", [new_permissions, username])

    #Commit
    mysql.connection.commit()

    #Close connection
    cursor.close()

    flash("Permissions Updated", 'success')

    return redirect(url_for('admin_page'))

#Delete user
@app.route('/delete_user/<string:username>', methods=['POST'])
@login_required
def delete_user(username):
    #Create cursor
    cursor = mysql.connection.cursor()

    #Execute
    if username == session['username']:
        flash("We can't delete our own account!", 'danger')
        return redirect(url_for('admin_page'))
    cursor.execute('DELETE FROM dashboard.users WHERE username = %s', [username])

    #Commit
    mysql.connection.commit()

    #Close connection
    cursor.close()

    flash("User succesfully deleted.", 'success')

    return redirect(url_for('admin_page'))

def test_graph():
    x = [1, 3, 5, 7]
    y = [2, 4, 6, 8]

    p = figure(plot_width=300,plot_height=300)

    p.circle(x, y, size=10, color='red', legend='circle')
    p.line(x, y, color='blue', legend='line')
    p.triangle(y, x, color='gold', size=10, legend='triangle')
    p.legend.click_policy='hide'
    script, div = components(p)
    return script, div

@app.route('/dashboard_1', methods=['GET', 'POST'])
@login_required
def dashboard1():
    script_test_graph, div_test_graph = test_graph()

    if session['permissions'] == 'admin' or session['permissions'] == 'developer':
        return render_template(
        'dashboard1.html',
        div_test_graph=div_test_graph,
        script_test_graph=script_test_graph
        )
    else:
        flash('Permission Denied', 'danger')
        return render_template('dashboard.html')
