from flask import Flask, render_template, redirect, session, g, request, jsonify
import requests
from forms import UserAddForm, LoginForm, SearchBreed, EditProfile
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


@app.route('/breeds')
def show_breeds():
    """Show a list of all breeds."""

    return render_template('breeds.html')


@app.route('/breed/<string:dog_name>', methods=['GET'])
def show_specific_breed(dog_name):
    """Show information about a specific breed."""

    return render_template('breed.html', dog=dog_name)


@app.route('/search', methods=['GET', 'POST'])
def search_breed():
    """Search for a breed."""

    form = SearchBreed()

    return render_template('search.html', form=form)


@app.route('/random', methods=['GET', 'POST'])
def random_breed():
    """Search for a breed."""

    return render_template('random.html')


@app.route('/edit/username', methods=['GET', 'POST'])
def update_profile():
    """Search for a breed."""

    if not g.user:
        return redirect('/')

    user = g.user
    form = EditProfile(obj=user)

    if form.validate_on_submit():
        if User.authenticate_user(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

    return render_template('edit.html', form=form, user_id=user.id)


@app.errorhandler(404)
def page_not_found(error):
    """Return a 404 not found page."""

    return render_template('404.html'), 404
