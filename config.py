class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flaskauthordb"
    JWT_SECRET_KEY = "authors"