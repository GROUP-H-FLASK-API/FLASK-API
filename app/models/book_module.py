from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = "books"  #customizing the table
    book_ID = db.Column(db.Integer,primary_key = True,unique = True,nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable = False,unique = True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable = False,unique = True)
    publication_date = db.Column(db.Integer,nullable = True)
    title = db.Column(db.String(30),nullable = False)
    pages = db.Column(db.Integer,nullable = False)
    price = db.Column(db.Integer,nullable = False)
    price_unit = db.Column(db.String(30),nullable = False,default ="UGX")
    publication_date = db.Column(db.Date,nullable = False)
    publisher =  db.Column(db.String(12))
    isbn = db.Column(db.String(30),nullable = True,unique = True)
    genre = db.Column(db.String(50),nullable = False)
    description = db.Column(db.String(230),nullable = False)
    image = db.Column(db.String(130),nullable = True)
        #strings composed of digits and hyphens
        #isbn uniquely identifies published books and it denotes the international standard book number
    author = db.relationship('Author', backref = "books")
    company = db.relationship('Company', backref = "books")
    #we use re
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    
    def __init__(self,book_ID,author_id,publication_date,title,created_at,updated_at):
        super(Book, self).__init__() #invoking the constructor of the super class
        self.book_ID = book_ID
        self.author_id = author_id
        self.publication_date = publication_date
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"Book {self.title}"