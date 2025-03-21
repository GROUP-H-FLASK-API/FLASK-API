from flask import Flask
from app.extensions import db, migrate, jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.author.author_controller import authors


def create_app(): #application factory function
    app = Flask(__name__) #instance
    app.config.from_object('config.Config') #registering the class

    db.init_app(app) #initialization of our database instance on our app variable
    migrate.init_app(app,db)
    jwt.init_app(app)



    #importing and registering models
    from app.models.author_module import Author
    from app.models.company_module import Company
    from app.models.book_module import Book
   

    #registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(authors)



    @app.route('/')
    def home():
        return "This is my web application"


    return app