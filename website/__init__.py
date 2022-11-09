from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    if not 'WEBSITE_HOSTNAME' in os.environ:
   # local development, where we'll use environment variables
        print("Loading config.development and environment variables from .env file.")
        app.config['SECRET_KEY'] = 'secret-key-goes-here'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
                                                    dbuser=os.environ['DBUSER'],
                                                    dbpass=os.environ['DBPASS'],
                                                    dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
                                                    dbname=os.environ['DBNAME']
                                                )
    else:
   # production
        print("Loading config.production.")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
                                                    dbuser=os.environ['DBUSER'],
                                                    dbpass=os.environ['DBPASS'],
                                                    dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
                                                    dbname=os.environ['DBNAME']
                                                )
        app.config['SECRET_KEY'] = 'secret-key-goes-here'


    
    db.init_app(app)

    #migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    # create_database(app)

    
    loging_manager = LoginManager()
    loging_manager.login_view = 'auth.login'
    loging_manager.init_app(app)

    @loging_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
