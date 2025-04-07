from flask import Blueprint, request, jsonify # Importing the Blueprint and request and jsonify classes from the flask module
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,   HTTP_201_CREATED, HTTP_200_OK , HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT  # Importing the HTTP status codes from the status_codes module
import validators  # Importing the validators module
from app.models.authors import Author  # Importing the Author class from the author_model module
from app.extensions import db, bcrypt  # Importing the db object from the extensions module
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity # Importing functions from the flask_jwt_extended module


# Creating a Blueprint instance
auth = Blueprint('auth', __name__, url_prefix='/api/v1/author') 



# User registration 
@auth.route('/register', methods=['POST']) # /register, this is the end point 

def register_user():
    data = request.json  #is the object that stores details from the request
    first_name = data.get('first_name')  
    last_name = data.get('last_name')  
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    biography = data.get('biography','')

  
      # Validations of the  incoming request 
    #working with the if statement to look for null values within the request
    if not first_name or not last_name or not contact or not email or not password: # Checking if all required fields are filled
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST
    
    # if not biography =="Author" and not biography:
    #     return jsonify({'error': 'Biography is required for authors'}), HTTP_400_BAD_REQUEST
    
    if len(password) < 8: # checking the password length
        return jsonify({'error': 'Password must be at least 8 characters'}), HTTP_400_BAD_REQUEST #JSONIFY is an API
    
    if not validators.email(email): # ensuring the correct email format 
        return jsonify({'error': 'Invalid email address'}), HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first(): # checking whether the email is already registered
        return jsonify({'error': 'Email already in use'}), HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first(): # shecking whether the contact is in use
        return jsonify({'error': 'Contact already in use'}), HTTP_409_CONFLICT
    
    
   #error handling using the try and except block  
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # Hashing the password, it is used to encrypt(hashing), we also decode to convert the password from one string to another
        #we hash to ensure that the password is not hacked on in other words for security purpose
        
        # Creating a new Author instance 
        author_1 = Author( first_name=first_name, last_name=last_name, 
                          contact=contact, email=email, password=hashed_password, 
                          biography=biography)    
        
        db.session.add(author_1)  # Adding the new Author instance to the database session
        db.session.commit()  # Committing the changes to the database   
        
        username = author_1.get_full_name() #first_name + ' ' + author_1.last_name
        return jsonify({
            'message': username + ' has been registered successfully as an'+ author_1.biography ,
            'user':{
                "first_name":author_1.first_name,
                "last_name":author_1.last_name,
                "email":author_1.email,
                "contact":author_1.contact,
                "biography":author_1.biography,
                "created_at":author_1.created_at,
                "updated_at":author_1.updated_at,
                
            }
            }), HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        #returning a response for the error
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
              
# User login        

@auth.post('/login')  # Defining a route for user login
def login():
    email = request.json.get('email')  # Extracting the email from the JSON data
    password = request.json.get('password')  # Extracting the password from the JSON data   
    
   # working with the error handling by using the try and except block
    try:
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), HTTP_400_BAD_REQUEST
    
        author = Author.query.filter_by(email=email).first()  # Querying the Author table to find the user with the specified email
        
        if author:
            is_correct_password = bcrypt.check_password_hash(author.password, password)
            refresh_token = create_refresh_token(identity=author.id)
        
            if is_correct_password: 
                access_token = create_access_token(identity=str(author.id))  # Creating an access token for the user
                refresh_token = create_refresh_token(identity=str(author.id))  # Creating a refresh token for the user


                return jsonify({
                    'author': {
                        'id':author.id,
                        'username': author.get_full_name(),
                        'email': author.email,
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    },
                    'message': 'you have sucessfully loged into you account'
                }) ,HTTP_200_OK

                # return jsonify({
                #     'message': 'You have successfully logged into your account',
                #     'access_token': access_token,
                #     'refresh_token': refresh_token
                #     }), HTTP_200_OK
                
            else:
                return jsonify({'message': 'Invalid password'}), HTTP_401_UNAUTHORIZED

        else:
            return jsonify({'message': 'Invalid email address'}), HTTP_401_UNAUTHORIZED
    
    
    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
        
# Refresh token
@auth.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True) # This decorator is used to protect routes that require a valid refresh token
def refresh():
    identity = str(get_jwt_identity())  # Extracting the identity from the JWT token
    access_token = create_access_token(identity=identity) # Creating a new access token
    return jsonify({'access_token': access_token}), HTTP_200_OK