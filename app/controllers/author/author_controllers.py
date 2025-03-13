from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORISED
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt,jwt
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required


Author = Blueprint('auth',__name__,url_prefix='/api/v1/author')


@Author.route('/register', methods=['POST'])
def register_author():
    data = request.json