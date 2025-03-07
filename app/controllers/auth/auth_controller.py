from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED
import validators
from app.models.author_module import Author
from app.extensions import db,bcrypt

#auth blueprint
auth = Blueprint('auth', __name__,
                        url_prefix='/api/v1/auth') #creating a new object


#user registration
@auth.route("/register", methods = ['POST'])
def register_user():

    #storing request values
    data = request.json
    fname = data.get("fname")
    lname = data.get("lname")
    contact = data.get("contact")
    email = data.get("email")
    password = data.get("password")
    biography = data.get("biography")
    created_at = data.get("created_at", "")
    updated_at = data.get("updated_at", "")


    #validations of the user requests
    if not fname or not lname or not contact or not email or not password:
        return jsonify({"Error":"All fields are required"}),HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({
            "Error":"Password should be atleast 8 characters"
        }),HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({
            "Error":"Email address is not valid"
        }),HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"Error":"Email address is already in use"}),HTTP_409_CONFLICT
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"Error":"Contact is already in use"}),HTTP_409_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash(password) #hashing the password
        #creating an Author
        new_author = Author(author_id=id,fname=fname,lname=lname,password=hashed_password,email=email,contact=contact,biography=biography,created_at=created_at,updated_at=updated_at)
        db.session.add(new_author)
        db.session.commit()

        #authorname
        author_name = new_author.get_full_name()


        return jsonify({"Message":author_name + "has been successfully created ",
                        "author":{
                            "id":new_author.author_id,
                            "first_name":new_author.fname,
                            "last_name":new_author.lname,
                            "email":new_author.email,
                            "contact":new_author.contact,
                            "biography":new_author.biography,
                            "created_at":new_author.created_at,
                            "updated_at":new_author.updated_at,
                                  }
                        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR