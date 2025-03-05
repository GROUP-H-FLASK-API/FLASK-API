from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, migrate
#application factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app,db)
    
#migrating models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book

    #index route
    @app.route('/')

    def index():
        return "HELLO"
        

    return app

