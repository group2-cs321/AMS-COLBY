from venv import create
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"
oauth = OAuth()

#creation of the Flash app object
def create_app():
    app = Flask(__name__)

    # TODO: Move this to a config file

    if not 'WEBSITE_HOSTNAME' in os.environ:
   # local development, where we'll use environment variables
        print("Loading config.development and environment variables from .env file.")
        app.config['SECRET_KEY'] = 'secret-key-goes-here'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
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

    #

    
    db.init_app(app)

    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    if not 'WEBSITE_HOSTNAME' in os.environ:
        create_database(app)

    
    loging_manager = LoginManager()
    loging_manager.login_view = 'auth.login'
    loging_manager.init_app(app)

    @loging_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Register remote app
    # Initialize app

    oauth = register_app(
        app = app,
        name = 'oura',
        client_id = "5QNUWHYTUNUEBPHK",
        client_secret = "QVACKSMIU2QX5JYGW6I6OFXXF2A3D6KG",
        auth_url = "https://cloud.ouraring.com/oauth/authorize",
        api_base_url = "https://api.ouraring.com/v2/",
        access_token_url = "https://api.ouraring.com/oauth/token"
        )

    from authlib.integrations.flask_client import token_update

    @token_update.connect_via(app)
    def on_token_update(sender, name, token, refresh_token=None, access_token=None):
        if refresh_token:
            item = OAuth2Token.query.filter_by(name=name, refresh_token=refresh_token).first()
        elif access_token:
            item = OAuth2Token.find.query.filter_by(name=name, access_token=access_token).first()
        else:
            return

        # update old token
        item.access_token = token['access_token']
        item.refresh_token = token.get('refresh_token')
        item.expires_at = token['expires_at']
        db.session.commit()

    
    return app

#create a database when no existing database is in place
def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')


def register_app(app, name, client_id, client_secret, auth_url, api_base_url, access_token_url):
    from .models import OAuth2Token
    from flask_login import current_user
    def fetch_token():
        model = OAuth2Token

        token = model.query.filter_by(
            name=name,
            user=current_user.id,
        ).first()


        return token.to_token()

    oauth.init_app(app)
    oauth.register( 
        name = name,
        client_id = client_id,
        client_secret = client_secret,
        authorize_url = auth_url,
        api_base_url = api_base_url,
        access_token_url = access_token_url,
        fetch_token = fetch_token
        )
    
    return oauth

