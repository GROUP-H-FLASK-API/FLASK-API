#buliding the author model
from app.extensions import db
from datetime import datetime #importing the datetime package

class Author(db.Model): # author class inherit  the model class from the db object
        __tablename__ = "authors" #customising and assigning it to author
        id = db.Column(db.Integer, primary_key = True,autoincrement = True,nullable=False) 
        first_name = db.Column(db.String(22),nullable=False)
        last_name = db.Column(db.String(22),nullable=False)
        contact = db.Column(db.String(10),nullable=False,unique=True)
        email = db.Column(db.String(22),nullable=False,unique=True)
        password = db.Column(db.String(255),nullable=False)
        biography = db.Column(db.String(255),nullable = True)
        created_at = db.Column(db.DateTime,default = datetime.now)
        updated_at = db.Column(db.DateTime,onupdate = datetime.now)
# create a constructor for our author model such that incase any instance or new author all the fields are  to be automatically required 
        def __init__(self,first_name,last_name,contact,email,password,biography):
          super(Author,self).__init__()
          self.first_name = first_name
          self.last_name = last_name
          self.contact = contact
          self.email = email
          self.password = password
          self.biography = biography
          
          
# creating a custom function that is to be concatnated the author's first name and last name
        def get_full_name(self):
             return f"{self.last_name} {self.first_name}"