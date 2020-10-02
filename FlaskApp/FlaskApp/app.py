from flask import Flask, render_template
from data import article_func

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
