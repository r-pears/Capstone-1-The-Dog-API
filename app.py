from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///dog-app'

@app.route('/')
def homepage():
    """Show the index page."""

    return render_template('index.html')
