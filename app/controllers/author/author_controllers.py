from flask import Blueprint,request,jsonify#importing the blue prints class from the flask module
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR
import validators 
from app.models.author_model import Author
from app.extensions import db,bcrypt
#create a new object
author = Blueprint('author', __name__,url_prefix='api/v1/author')

#User registration

@author.route('/register_user',method =['POST'])
def register_user ():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get ('contact')
    email = data.get('email')
    password = data.get('password')
    image = data.get(' image')
    biography = data.get('biography')

    #validations of the incoming request
    if not first_name or not last_name or not contact or not email or not password or not image:
        return jsonify({"error":"All fields are required"}), HTTP_400_BAD_REQUEST
    if type =='author' and not biography:
        return jsonify({'error':'Enter your author biography'}),HTTP_400_BAD_REQUEST
    if len(password) < 8:
        return jsonify({'error':'Password is too short '}), HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return jsonify({'error':'email is not valid '}), HTTP_400_BAD_REQUEST
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'email address in use'}), HTTP_409_CONFLICT
    if Author.query.filter_by(contact = contact).first() is not None:
        return jsonify({'error':'Conact already in use '}), HTTP_409_CONFLICT
    try:
        #hashing the password
        hashed_pasword = bcrypt.generate_password_hash(password)
        #creating a new user
        new_user = Author(firstname = first_name,last_name = last_name,password = hashed_pasword,email=email,contact=contact,biography=biography)
        db.session.add(new_user)
        db.session.commit()

         #user name
        username = new_user
        return jsonify({
            'message': 'login succeful'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify ({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR


    

    
    
