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
from FlaskApp.blueprints.auth import login_required
from FlaskApp.blueprints.dashboard import dashboard_page

#Articles page
articles_page = Blueprint('articles_page', __name__,
                        template_folder='templates')
@articles_page.route('/articles') #the url in the app.
@login_required
def articles():
    #Create cursor
    cursor = db.connection.cursor()

    #Get articles
    result = cursor.execute("SELECT * FROM dashboard.articles")

    articles = cursor.fetchall()

    if result > 0:
        return render_template('articles/articles.html', articles=articles)
    else:
        return render_template('articles/articles.html')

#Single article selection
article_page = Blueprint('article_page', __name__,
                        template_folder='templates')
@article_page.route('/article/<string:id>') #the url in the app.
@login_required
def article(id):
    cursor = db.connection.cursor()

    #Get articles
    result = cursor.execute("SELECT * FROM dashboard.articles WHERE id = %s", [id])
    article = cursor.fetchone()

    return render_template('articles/article.html', article=article)

#Article Form Class
class ArticleForm(Form):
    title = StringField('Name',[validators.Length(min=1, max=200)])
    body = TextAreaField('Text',[validators.Length(min=30)])

#Add article
add_article_action = Blueprint('add_article_action', __name__,
                        template_folder='templates')
@add_article_action.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        #Create DictCursor
        cursor = db.connection.cursor()

        #Execute
        cursor.execute("INSERT INTO dashboard.articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        #Commit
        db.connection.commit()

        #Close connection
        cursor.close()

        flash('Documentation Created', 'success')

        return redirect(url_for('dashboard_page.dashboard'))
    return render_template('articles/add_article.html', form=form)

#Edit article
edit_article_action = Blueprint('edit_article_action', __name__,
                        template_folder='templates')
@edit_article_action.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    #Create cursor
    cursor = db.connection.cursor()

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
        cursor = db.connection.cursor()

        #Execute
        cursor.execute("UPDATE dashboard.articles SET title = %s, body = %s, updated=CURRENT_TIMESTAMP() WHERE id = %s", (title, body, id))

        #Commit
        db.connection.commit()

        #Close connection
        cursor.close()

        flash('Documentation Updated', 'success')

        return redirect(url_for('dashboard_page.dashboard'))
    return render_template('articles/add_article.html', form=form)

#Delete article
delete_article_action = Blueprint('delete_article_action', __name__,
                        template_folder='templates')

@delete_article_action.route('/delete_article/<string:id>', methods=['POST'])
@login_required
def delete_article(id):
    #Create cursor
    cursor = db.connection.cursor()

    #Execute
    cursor.execute("DELETE FROM dashboard.articles WHERE id = %s", [id])

    #Commit
    db.connection.commit()

    #Close connection
    cursor.close()

    flash('Documentation Deleted', 'success')

    return redirect(url_for('dashboard_page.dashboard'))
