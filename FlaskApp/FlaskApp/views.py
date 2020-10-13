from flask import Blueprint

from FlaskApp import app, db #db is a mysql instance, shown in __init__.py
from FlaskApp.blueprints.base import  about_page, home_page
from FlaskApp.blueprints.auth import register_page, login_page, logout_page, login_required
from FlaskApp.blueprints.dashboard import dashboard_page, dashboard_demo_page
from FlaskApp.blueprints.admin import admin_page, delete_user_action, update_permissions_action
from FlaskApp.blueprints.articles import articles_page, article_page, add_article_action, edit_article_action, delete_article_action

#Handle the homepages with blueprints
app.register_blueprint(home_page)
app.register_blueprint(about_page)

#Handle the authentication with blueprints
app.register_blueprint(register_page)
app.register_blueprint(login_page)
app.register_blueprint(logout_page)

#Handle the articles/documentation pages with blueprints
app.register_blueprint(articles_page)
app.register_blueprint(article_page)
app.register_blueprint(add_article_action)
app.register_blueprint(edit_article_action)
app.register_blueprint(delete_article_action)

#Handle the admin page with blueprints
app.register_blueprint(admin_page)
app.register_blueprint(delete_user_action)
app.register_blueprint(update_permissions_action)

#Handle the dashboards with blueprints
app.register_blueprint(dashboard_page)
app.register_blueprint(dashboard_demo_page)
