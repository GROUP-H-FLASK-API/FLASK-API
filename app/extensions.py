from flask_sqlalchemy import SQLAlchemy #from flask_sqlalchemy model we create a class called SQLAlchemy
from flask_migrate import Migrate #importing a class called migrate 
#that helps to push our work to db so that author is there, book is there
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import Flask

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
