from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

my_app = Flask(__name__)
my_app.config.from_object(Config)

my_db = SQLAlchemy(my_app)

migration = Migrate(my_app, my_db)

login_manager = LoginManager(my_app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from market import routes
