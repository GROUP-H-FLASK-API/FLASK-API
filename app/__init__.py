from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, migrate,jwt
from app.controllers.auth.auth_controllers import auth
from app.controllers.author.author_controllers import author
#application factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    
#migrating models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book


    app.register_blueprint(auth)
    app.register_blueprint(author)
    #index route
    @app.route('/')

    def index():
        return "HELLO"
        

    return app

