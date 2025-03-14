from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


migrate = Migrate() #migrate instance
db = SQLAlchemy()  #db instance
bcrypt = Bcrypt() #new object of the Bcrypt() class
jwt = JWTManager()