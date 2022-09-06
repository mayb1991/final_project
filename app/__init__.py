from flask import Flask
from config import Config
from flask_moment import Moment
from flask_login import LoginManager
from .auth.routes import auth
from .models import User




app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager()


moment = Moment(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth)

from .models import db

login.init_app(app)
login.login_view = 'auth.login'

from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)


from . import routes
from app import models