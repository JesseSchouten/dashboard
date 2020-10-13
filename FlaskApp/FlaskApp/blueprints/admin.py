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

admin_page = Blueprint('admin_page', __name__,
                        template_folder='templates')

@admin_page.route('/admin')
@login_required
def admin():
    #Create cursor
    cursor = db.connection.cursor()

    #Get articles
    result = cursor.execute("SELECT id, name, email, username, permissions FROM dashboard.users;")

    users = cursor.fetchall()

    if result > 0:
        return render_template('admin/admin.html', users=users)
    else:
        return render_template('admin/admin.html')

update_permissions_action = Blueprint('update_permissions_action', __name__,
                        template_folder='templates')

#Update permissions in admin page
@update_permissions_action.route('/update_permissions/<string:username>_<string:new_permissions>', methods=['POST'])
@login_required
def update_permissions(username, new_permissions):
    #Create cursor
    cursor = db.connection.cursor()

    #Execute
    if username == session['username']:
        flash("We can't update our own permissions!", 'danger')
        return redirect(url_for('admin_page.admin'))
    cursor.execute("UPDATE dashboard.users SET permissions= %s, updated = CURRENT_TIMESTAMP() WHERE username = %s;", [new_permissions, username])

    #Commit
    db.connection.commit()

    #Close connection
    cursor.close()

    flash("Permissions Updated", 'success')

    return redirect(url_for('admin_page.admin'))

#Delete user in admin page
delete_user_action = Blueprint('delete_user_action', __name__,
                        template_folder='templates')

@delete_user_action.route('/delete_user/<string:username>', methods=['POST'])
@login_required
def delete_user(username):
    #Create cursor
    cursor = db.connection.cursor()

    #Execute
    if username == session['username']:
        flash("We can't delete our own account!", 'danger')
        return redirect(url_for('admin_page.admin'))
    cursor.execute('DELETE FROM dashboard.users WHERE username = %s', [username])

    #Commit
    db.connection.commit()

    #Close connection
    cursor.close()

    flash("User succesfully deleted.", 'success')

    return redirect(url_for('admin_page.admin'))
