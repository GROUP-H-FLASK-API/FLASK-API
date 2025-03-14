from app.extensions import db
from datetime import datetime


class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.Integer,primary_key = True,autoincrement=True ,nullable = False,unique = True)
    fname = db.Column(db.String(50),nullable = False)
    lname = db.Column(db.String(100),nullable = False)
    contact = db.Column(db.String(10),nullable = False, unique = True)
    email = db.Column(db.String(85),nullable = False, unique = True)
    password = db.Column(db.String(255),nullable = False)
    biography = db.Column(db.String(255),nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, onupdate = datetime.now)


    def __init__(self,fname,lname,email,contact,biography,password,created_at,updated_at):
        super(Author, self).__init__() #invoking the constructor of the super class
        self.fname = fname
        self.lname = lname
        self.contact = contact
        self.email = email
        self.password =  password
        # self.author_id = author_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.biography = biography


    def get_full_name(self):
        return f"{self.lname} {self.fname}"