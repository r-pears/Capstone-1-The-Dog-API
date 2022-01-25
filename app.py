from flask import Flask, render_template, redirect, session, g, request, jsonify
import requests
from forms import UserAddForm, LoginForm
from models import db, connect_db, User
from sqlalchemy.exc import IntegrityError

CURRENT_USER_KEY = "current_user"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dog-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)

@app.before_request
def add_user_to_global():
    """If the user is logged in, add the current user to Flask global."""

    if CURRENT_USER_KEY in session:
        g.user = User.query.get(session[CURRENT_USER_KEY])
    
    else:
        g.user = None
    

def do_login(user):
    """Log in user."""

    session[CURRENT_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]


@app.route('/')
def homepage():
    """Show the index page."""

    if g.user:

        return render_template('home.html')
    
    else:
        return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    """Handle user registration."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            return render_template('register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate_user(form.username.data, form.password.data)

        if user:
            do_login(user)
            return redirect('/')
        
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    do_logout()

    return redirect("/")


@app.route('/user/<int:user_id>')
def show_user(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('user_profile.html', user=user)


@app.errorhandler(404)
def page_not_found(error):
    """Return a 404 not found page."""

    return render_template('404.html'), 404
