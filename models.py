from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
  """Connect this database to provided Flask app. """

  db.app = app
  db.init_app(app)


class User(db.Model):
  """User in the system."""

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.Text, nullable=False, unique=True)
  email = db.Column(db.Text, nullable=False, unique=True)
  password = db.Column(db.Text, nullable=False)

  @classmethod
  def register(cls, username, email, password):
    """Register a new user. Hashes password and adds user."""

    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')

    user = User(
      username=username,
      email=email,
      password=hashed_password
    )

    db.session.add(user)
    return user

  @classmethod
  def authenticate_user(cls, username, password):
    """Authenticate a returning user."""

    user = cls.query.filter_by(username=username).first()

    if user:
        is_auth = bcrypt.check_password_hash(user.password, password)
        if is_auth:
            return user

    return False
