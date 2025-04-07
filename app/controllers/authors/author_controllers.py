from flask import Blueprint, request, jsonify # Importing the Blueprint and request and jsonify classes from the flask module
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,   HTTP_201_CREATED, HTTP_200_OK , HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT,HTTP_403_FORBIDDEN # Importing the HTTP status codes from the status_codes module
import validators  # Importing the validators module
from app.models.authors import Author  # Importing the Author class from the author_model module
# from app.models.book import Book
from app.extensions import db, bcrypt  # Importing the db object from the extensions module
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity # Importing functions from the flask_jwt_extended module


author = Blueprint('authors', __name__, url_prefix='/api/v1/authors')

#get all authors
@author.get('/get_all_authors')
def getallauthors():


    try:    

        all_authors = Author.query.all()

        authors_data = []

        for author in all_authors:
            author_info ={
                "id": author.id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "username": author.get_full_name(),
                "email":author.email,
                "contact":author.contact,
                "created_at":author.created_at,
                "companies":[],
                "books":[]
                
            }

            authors_data.append(author_info)
            # if hasattr(author,'books'):
            #     author_info['books']=[{'id':Book.id,'title':Book.title,'isbn':Book.isbn,'description':Book.decription}]

        return jsonify ({
            "message":"All authors retrieved successfully",
            "authors": authors_data

        }) , HTTP_200_OK
    


    except Exception  as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#Get author by id
@author.get('/<int:author_id>')
@jwt_required()
def get_author(author_id):

    try:    
       
        author = Author.query.get(author_id)
        if not author:
            return jsonify({'error':'author not found'}),HTTP_404_NOT_FOUND
        books = []
        companies = []

        if hasattr(author, 'books'):
            books = [{'id':books.id,'title':books.title,'isbn':books.isbn,'description': books.description} for books in author.books]
        
        if hasattr(author,'companies'):
            companies = [{'id':companies.id,'name':companies.name,'origin':companies.origin,'description':companies.description}for companies in author.companies]
           

        return jsonify ({
            "message":"All authors retrieved successfully",
            "authors": {
                "id": author.id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "username": author.get_full_name(),
                "email":author.email,
                "contact":author.contact,
                'biography':author.biography,
                "created_at":author.created_at,
                'companies':companies,
                'books':books

            }

        }) , HTTP_200_OK
    


    except Exception  as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


# #updating authors details

@author.route('/edit/<int:id>',methods=['PUT','PATCH'])
@jwt_required()
def updateAuthorsDetails(id):

    try:  
        current_author = get_jwt_identity()
        loggedInAuthor = Author.query.filter_by(id=current_author).first()

        authors = Author.query.filter_by(id=id).first()  
        if not authors:
            return jsonify({'error':'author not found'}),HTTP_404_NOT_FOUND
        
        else:
            first_name = request.get_json().get('first_name',authors.first_name)
            last_name = request.get_json().get('last_name',authors.last_name)
            email = request.get_json().get('email',authors.email)
            contact = request.get_json().get('contact',authors.contact)
            biography = request.get_json().get('biography',authors)
            if 'password' in request.json:
                hashed_password = bcrypt.generate_password_hash(request.json.get('password'))
                authors.password = hashed_password

# checking for already in use details
            if email!= authors.email and Author.query.filter_by(email=email).first():
               return jsonify({
                   "error":"Email address already in use"
               }), HTTP_409_CONFLICT
            
            if contact!= authors.contact and Author.query.filter_by(contact=contact).first():
               return jsonify({
                   "error":"contact already in use"
               }), HTTP_409_CONFLICT

            authors.first_name = first_name
            authors.last_name = last_name
            authors.email = email
            authors.contact = contact
            authors.biography = biography

            db.session.commit()

            authors_name = authors.get_full_name()

            return jsonify({
                'message': authors_name + "details have been successfuly updated",
                'author':{
                    'id':authors.id,
                    'first_name':authors.first_name ,
                    'last_name': authors.last_name,
                    'email':authors.email,
                    'contact':authors.contact,
                    'biography':authors.biography 

                }


            }), HTTP_200_OK
    


    except Exception  as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


#deleting user
@author.delete('/<int:author_id>',)
@jwt_required()
def delete_author(author_id):

    try:  
        current_author = get_jwt_identity()
        loggedInAuthor = Author.query.filter_by(id=current_author).first()

        author = Author.query.filter_by(id=id).first() 

        if not author:
            return jsonify({'error':'author not found'}),HTTP_404_NOT_FOUND
        
        elif loggedInAuthor.author!='admin':
            return jsonify({'error':'you are not authorized to delete the author details'}),HTTP_403_FORBIDDEN
        
        else:
            # delete associated companies
            for company in author.companies:
                db.session.delete(company)

                 # delete associated book
            for book in author.books:
                db.session.delete(book)

                db.session.delete(author)
           
            db.session.commit()

            

            return jsonify({
                'message':'author deleted succefully' 
            }), HTTP_200_OK
    


    except Exception  as e:
        return jsonify({
            "error":str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR




