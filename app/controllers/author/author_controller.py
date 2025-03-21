from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_module import Author
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token

#authors blueprint
authors = Blueprint('authors', __name__,
                        url_prefix='/api/v1/authors') #creating a new object
#getting all authors from the database
@authors.get('/')
@jwt_required()
def getAllAuthors():



    # email = request.json.get("email")
    # password = request.json.get("password")

    try:

        all_authors = Author.query.all()


        authors_data = []

        for author in all_authors:
            author_info = {
                "id" : author.author_id,
                "first_name" : author.fname,
                "last_name" : author.lname,
                "author_name" : author.get_full_name(),
                "email" : author.email,
                "contact" : author.contact,
                "created_at" : author.created_at
                }
            
            authors_data.append(author_info)

        return jsonify({
            "Message": "All Authors retrieved successfully",
            "total authors": len(authors_data),
            "authors":authors_data
        }),HTTP_200_OK #serializing the data enables us have a variable that can be converted to jsony easily
        
    except Exception as e:
        return  jsonify({
            "Error":str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    
#getting an author by id
# @authors.get('/author/<int:author_id>')
# @jwt_required()
# def getAuthor(author_id):
        

#         try:
#             author = Author.query.filter_by(author_id=author_id).first()
#             books = []
#             companies = []
            
#             if hasattr(author,"books"):
#                  books = [{"id"=book.book_ID,"title"=book.title,"pages"=book.pages}]

#         return jsonify({
#             "Message": "All Authors retrieved successfully",
#             "total authors": len(authors_data),
#             "authors":authors_data
#         }),HTTP_200_OK