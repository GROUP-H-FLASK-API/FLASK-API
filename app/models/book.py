
from app.extensions import db
from datetime import datetime


class Book(db.Model): #book sub_class inherit  the model class from the db object
        __tablename__ = 'books' #customising the table name and the creating columns for the table
        id = db.Column(db.Integer,primary_key = True)
        title = db.Column(db.String(15))
        decription = db.Column(db.String(5))
        isbn = db.Column(db.String(30))
        pages = db.Column(db.String(3000))
       #  author_id = db.Column(db.Integer,db.ForeignKey('Author.id'))
       #  company_id = db.Column(db.Integer,db.ForeignKey('Company.id'))
        created_at = db.Column(db.DateTime,default = datetime.now)
       #  author = db.relationship('Author', backref = 'book')
       #  company = db.relationship('Company', backref = 'book')
        updated_at = db.Column(db.DateTime,onupdate = datetime.now)
        
 # create a constructor for our book model such that incase of new objects  all the fields/attributes are  to be automatically required        
        def __init__(self,title,description,pages,user_id):
         super(Book,self).__init__() #invoking the init method from  db.model super class
         self.title = title
         self.descrption = description
         self.pages = pages
         self.user_id = user_id



         def __repr__(self):
              return f"Book {self.title}"
           