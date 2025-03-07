from app.extensions import db
from datetime import datetime


class Company(db.Model):
    __tablename__ = "companies"  #customizing the table
    company_id = db.Column(db.Integer,primary_key = True, nullable = False,unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable = False,unique = True)
    Author = db.relationship('Author', backref = "Companies") #relationship function, backref allows us to access author from companies
    contact = db.Column(db.String(10), nullable = False,unique = True)
    name = db.Column(db.String(25), nullable = False,unique = True)
    location = db.Column(db.String(14), nullable = True,unique = False)
    email = db.Column(db.String(40), nullable = False,unique = True)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    
    def __init__(self,company_id,author_id,contact,name,location,email,created_at,updated_at):
        super(Company, self).__init__() #invoking the constructor of the super class
        self.company_id = company_id
        self.author_id = author_id
        self.name = name
        self.contact = contact
        self.location = location
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at


    def __repr__(self): #string representation for the companies that will be created
        return f"{self.name} {self.location}"