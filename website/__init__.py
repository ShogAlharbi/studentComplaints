from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_babel import Babel


babel = Babel()

db = SQLAlchemy()
DB_NAME = "database.db"

def create_database(app):
    if not path.exists('website/'+DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database')

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY']='My duck and your duck'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # languages
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']

    babel.init_app(app)
    db.init_app(app)

#Set up login
    Login_manager= LoginManager()
    Login_manager.login_view = 'auth.login'
    Login_manager.init_app(app)

    @Login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))
 #Blueprints login
    from .models import Note
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    with app.app_context():
        db.create_all()
        create_database(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

    @app.route('/')
    def home():
        lang = request.args.get('lang', 'en')
        if lang == 'ar':
            return "مرحباً بك في تطبيق الشكاوى"
        else:
            return "Welcome to the Complaints Application"
    
    return app
