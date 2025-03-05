from app.extensions import db
from datetime import datetime
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(50))
    origin = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default =datetime.now())
    updated_at = db.Column(db.DateTime, default = datetime.now())
    specialisation = db.Column(db.String(100))
    def __init__(self,id, name, contact,email,origin,created_at,updated_at,specialisation):
        self.name = name
        self.id = id
        self.contact = contact
        self.email = email
        self.origin = origin
        self.created_at = created_at
        self.updated_at =updated_at


