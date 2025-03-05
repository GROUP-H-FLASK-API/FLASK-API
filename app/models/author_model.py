from app.extensions import db
from datetime import datetime
class Author (db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.String(30))
    contact = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default = datetime.now())

    def __init__(self,name, id,age,contact,email,address): #constractor
        self.name = name
        self.id = id
        self.age = age
        self.contact = contact
        self.email = email
        self.address = address
       

    