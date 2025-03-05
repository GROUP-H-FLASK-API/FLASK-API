from app.extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.string(100), unique=True)
    origin = db.Column(db.string(100))
    description = db.Column(db.string(100))
    user_id = db.Column(db.Integer(100),db.ForeignKey('user_id'))
    user = db.relationship("user",backref="companies")
    created_at = db.Column(db.Datetime,defaul=datetime.now())
    update_at = db.Column(db.Datetime,defaul=datetime.now())

    def __init__(self,name,origin,description,user_id):
     super(Company,self).__init__()
     self.name = name
     self.origin = origin
     self.description = description
     self.user_id = user_id
     

     def __repo__(self):
        return f"<Company(name '{self.name})', origin'{self.origin}')>"