from flask import Flask, render_template, flash, redirect
from forms import UserAddForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///dog-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True


@app.route('/')
def homepage():
    """Show the index page."""

    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken")
            return render_template('register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('register.html', form=form)
