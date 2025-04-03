from app.extensions import db
from datetime import datetime
class Book(db.Model):
    __tablename__ ="Book"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(30))
    pages = db.Column(db.String(50))
    price = db.Column(db.String(50))
    description = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, default = datetime.now)
    def __init__(self,title,pages, price, description,no_of_pages,authorsname,publishersname,publicationdate):
        self.title = title
        self.pages = pages
        self.authorsname = authorsname
        self.publishersname = publishersname
        self.publicationdate = publicationdate
        self.description = description
        self.no_of_pages = no_of_pages
        self.price = price
   