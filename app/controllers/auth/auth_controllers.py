from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORISED
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt,jwt
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required



#auth blueprint
auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth')

#user registration

@auth.route('/register', methods=['POST'])
def register_author():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    biography = data.get('biography', '') 



#validation of the incoming request
    if not first_name or not last_name or not password or not email:
        return jsonify({"error":"All fields are required"}), HTTP_400_BAD_REQUEST
   
    if not biography == "Author"  and not biography:
        return jsonify({"error":"Enter your author biography"}),HTTP_400_BAD_REQUEST
    
    if len(password)< 8:
        return jsonify({"error":"Password is too short"}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({"error":"Email is not valid"}),HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email = email).first() is not None:
        return jsonify({"error":"Email Address already  in use"}),HTTP_409_CONFLICT 
    

    if Author.query.filter_by(contact = contact).first() is not None:
        return jsonify({"error":"Contact already in use"}),HTTP_409_CONFLICT 
    
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #creating a new user
        new_user = Author(first_name=first_name,last_name=last_name,password= hashed_password,email=email,contact=contact,biography=biography)
        db.session.add(new_user)
        db.session.commit()

        User_name = new_user.get_full_name()

        return jsonify ({
            'message':User_name + "has been successfully created as an" + new_user.biography,
            'User':{
                "first_name":new_user.first_name,
                "last_name":new_user.last_name,
                "password":new_user.password,
                "email":new_user.email,
                "biography":new_user.biography,
                "contact":new_user.contact,
                "created_at":new_user.created_at,
                "updated_at":new_user.updated_at,
            }
            }),HTTP_201_CREATED
    

    except Exception as e:
         db.session.rollback()
         return jsonify({"error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR



# user login
@auth.post('/login')
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    try:

        if not email or not password:
            return jsonify ({"message":"email and password are required"}),HTTP_400_BAD_REQUEST
        
        author = Author.query.filter_by(email=email).first()

        if author:
            is_correct_password = bcrypt.check_password_hash(author.password,password)
        
            if is_correct_password:
               access_token = create_access_token(identity= str(author.id))
               refresh_token =create_refresh_token(identity= str(author.id))

               return jsonify({
    'author': {
        'id': author.id,
        'username': author.get_full_name(),
        'email': author.email,
        'access_token': access_token,
        'refresh_token': refresh_token
    }, 
    "message":'you have succrssfully loged into your account'
}), HTTP_200_OK
        
            else:
                return jsonify({"message":"invalid password"})


        else:
           return jsonify({"message":"invalid email address"}),HTTP_401_UNAUTHORISED
    


    except Exception as e:
        return jsonify({
        "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    


@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity =str(get_jwt_identity())
    access_token = create_access_token(identity=str(identity))
    return jsonify({'access_token':access_token}),HTTP_200_OK

