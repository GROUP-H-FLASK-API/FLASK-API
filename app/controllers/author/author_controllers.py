from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORISED
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt,jwt
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required



# Author blueprint
author = Blueprint('author', __name__, url_prefix='/api/v1/authors')

# Get all authors
@author.get('/get_all_authors')
def get_all_authors():

    
    try:
        authors = Author.query.all()
        authors_data = []

        for author in authors:
            author_info = {
            "id": author.id,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "contact": author.contact,
            "email": author.email,
            "biography": author.biography,
            "created_at": author.created_at,
            "updated_at": author.updated_at
        }

        authors_data.append(author_info)

        return jsonify({
            "message": "Authors retrieved successfully",
            "authors": author_info
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

# # Get a single author by ID
@author.get('/<int:author_id>', )
def get_author(author_id):
      try:
          author = Author.query.get(author_id)
          if not author:
              return jsonify({"error": "Author not found"}),HTTP_400_BAD_REQUEST

          return jsonify({
              "message": "Author retrieved successfully",
              "author": {
                  "id": author.id,
                  "first_name": author.first_name,
                  "last_name": author.last_name,
                  "contact": author.contact,
                  "email": author.email,
                  "biography": author.biography,
                  "created_at": author.created_at,
                  "updated_at": author.updated_at
              }
          }), HTTP_200_OK

      except Exception as e:
         return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# # Update an author
@author.put('/<int:author_id>',)
@jwt_required()
def update_author(author_id):
    try:
        author = Author.query.get(author_id)
        if not author:
             return jsonify({"error": "Author not found"}),HTTP_400_BAD_REQUEST

        data = request.json
        author.first_name = data.get('first_name', author.first_name)
        author.last_name = data.get('last_name', author.last_name)
        author.contact = data.get('contact', author.contact)
        author.email = data.get('email', author.email)
        author.biography = data.get('biography', author.biography)

        db.session.commit()

        return jsonify({
             "message": "Author updated successfully",
             "author": {
                 "id": author.id,
                 "first_name": author.first_name,
                 "last_name": author.last_name,
                 "contact": author.contact,
                 "email": author.email,
                 "biography": author.biography,
                 "created_at": author.created_at,
                 "updated_at": author.updated_at
             }
         }), HTTP_200_OK

    except Exception as e:
         db.session.rollback()
         return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# # Delete an author
@author.delete('/<int:author_id>',)
@jwt_required()
def delete_author(author_id):
    try:
         author = Author.query.get(author_id)
         if not author:
             return jsonify({"error": "Author not found"}), HTTP_400_BAD_REQUEST

         db.session.delete(author)
         db.session.commit()

         return jsonify({"message": "Author deleted successfully"}), HTTP_400_BAD_REQUEST


    except Exception as e:
     db.session.rollback()
    return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR