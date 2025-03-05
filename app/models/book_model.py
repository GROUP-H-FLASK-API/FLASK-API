
from app.extensions import db
from datetime import datetime


class Book (db.Model):
        __tablename__ = 'book'
        id = db.column(db.integer,primary_key = True)
        title = db.column(db.string(15))
        decription = db.column(db.string(5))
        isbn = db.column(db.string(30))
        pages = db.column(db.string(3000))
        user_id = db.column(db.Integer,db.ForeignKey('users.id'))
        company_id = db.column(db.Integer,db.ForeignKey('companies.id'))
        created_at = db.Column(db.DateTime,default = datetime.now())
        user = db.relationship('User', backref = 'book')
        company = db.relationship('Company', backref = 'book')
        updated_at = db.Column(db.DateTime,onupdate = datetime.now())
        
        
        def __init__(self,title,description,pages,user_id):
         super(Book,self).__init__()
         self.title = title
         self.descrption = description
         self.pages = pages
         self.user_id = user_id



         def __repr__(self):
              return f"<Book {self.title}"
           


         
# instance
book_1 = Book("betryal","2000000","3yhuefd9e8342809","546","2003")
book_1.books_info()