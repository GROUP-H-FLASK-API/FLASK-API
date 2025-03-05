from flask import Flask
from app.extensions import db,migrate

#Application factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    db.init_app(app)
    migrate.init_app(app,db)

    #Registering models
    from app.models.author_model import Author
    from app.models.company_model import company
    from app.models.book_model import Book

    #index route
    @app.route("/")
    def home():
        return "Hello,Flask!"
    
    return app # returns the flask app instance

    #register blue print
    app.register_blueprint(Author)
    app.register_blueprint(Book)
    app.register_blueprint(company)