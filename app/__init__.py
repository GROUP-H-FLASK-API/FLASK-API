# the init file tells python to treate our folder as a package. it also allows us import moduels
#useful if you want to set up certain configurations, create global variables, or define certain logic
# that should run when any part of the package is accessed.

from flask import Flask
from app.extensions import db , migrate, jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.controllers.auth.auth_controllers import auth
from app.controllers.authors.author_controllers import author


#Application factory function to define the app instance
def create_app():
    app = Flask(__name__) 
    app.config.from_object('config.Config') #registering the class within the application factory function 


    db.init_app(app) #inialisation of the app instance to the application instance
    migrate.init_app(app,db) #initalise migrate_object with in 
    jwt.init_app(app)

    # Registering models
    from app.models.authors import Author
    from app.models.company import Company
    from app.models.book import Book

    #registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(author)

    #index route
    @app.route("/") #testing the application with a route that returns a string litral
    def home():
        return "Hello,Flask!"
    
    return app # returns the flask app instance

    # #register blue print
    app.register_blueprint(Author)
    app.register_blueprint(Book)
    app.register_blueprint(company)