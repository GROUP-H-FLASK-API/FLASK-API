from app.extensions import db #import the db object
from datetime import datetime #importing the date time

class Company(db.Model):  # company class inherit  the model class from the db object
    __tablename__ = "company" #customising the table name and the create diffrent Columns for the table
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True)
    origin = db.Column(db.String(100))
    description = db.Column(db.String(100))
    # author_id = db.Column(db.Integer,db.ForeignKey('Author.id'))
    # author = db.relationship("Author",backref="Companies")
    created_at = db.Column(db.DateTime,default=datetime.now)
    update_at = db.Column(db.DateTime,onupdate=datetime.now)


# create a constructor for our company model such that incase of new objects  all the fields/attributes are  to be automatically required 
    def __init__(self,name,origin,description,user_id):
     super(Company,self).__init__()
     self.name = name
     self.origin = origin
     self.description = description
     self.user_id = user_id
     

#string presentation for the companies to be created 
    def __repo__(self): #working with the repo function
        return f"{self.name} {self.origin}"