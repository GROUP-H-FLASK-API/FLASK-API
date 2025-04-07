#seting up the configaration keys

class Config: #this class will allow us centralise the applications configarations
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flask_author_api_db" #SQL URI pass key and the  connection string

        JWT_SECRET_KEY = "author"


