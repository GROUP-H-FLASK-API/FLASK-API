from app.extensions import db
from datetime import datetime
class Author(db.Model):
    __tablename__ = "Author"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact = db.Column(db.String(50),nullable=True)
    email = db.Column(db.String(100),nullable=True)
    password = db.Column(db.String(255), nullable=False)
    biography  = db.Column(db.String(255),nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime,onupdate=datetime.now)

    def __init__(self,name, id,age,contact,email,password,last_name,first_name): #constractor
        self.name = name
        self.id = id
        self.age = age
        self.contact = contact
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        
       

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"