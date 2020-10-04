from flask import Flask, render_template, flash, request, redirect, url_for, session, logging
from data import article_func
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Alkmaar12!'
app.config['MYSQL_DB'] = 'authenticate'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

article_list = article_func()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about') #the url in the app.
def about():
    return render_template('about.html')

@app.route('/articles') #the url in the app.
def articles():
    return render_template('articles.html', articles = article_list)

@app.route('/article/<string:id>') #the url in the app.
def article(id):
    return render_template('article.html', id=id)

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1, max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match!'),
    ])
    confirm = PasswordField('Confirm Password')

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
            cur.execute("INSERT INTO authenticate.users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username,(password)))
        except Exception as e:
            if type(e).__name__ == 'IntegrityError':
                flash('This user already exists!')
                return render_template('register.html', form=form)
            else:
                flash('An unknown error occurred, try again!')
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
        result = cursor.execute("SELECT * FROM authenticate.users WHERE BINARY username = %s", [username])

        if result > 0:
            #Get stored hash
            data = cursor.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
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

#logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', show_sidebar=True)


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.run(debug=True)
