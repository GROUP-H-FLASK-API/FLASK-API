from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN
import validators
from app.models.author_model import Author
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from app.extensions import db,bcrypt
from sqlalchemy import or_

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
@authors.get('/author/<int:author_id>')
@jwt_required()
def getAuthor(author_id):
        
        

        try:
            author = Author.query.get(author_id)

          #   books = []
            companies = []

          #   if hasattr(author, "books"):
          #        books = [{ 'id': book.book_ID, 'title':book.title,'price':book.price,'genre':book.genre, 'price_unit':book.price_unit, 'description':book.description, 'publisher':book.publisher, 'publication':book.publication_date, 'image':book.image,'created_at':book.created_at} for book in author.books]

            if hasattr(author, "companies"):
                 companies = [{ 'id': company.company_id, 'name':company.name,'contact':company.contact,'email':company.email, 'location':company.location,'created_at':company.created_at} for company in author.companies]

            if not author:
                 return jsonify({
                      "Error":"Author not found"
                 }), HTTP_404_NOT_FOUND
            return jsonify({
                 "Message": "Author retrieved successfully",
                 "authors":{
                      "id":author.author_id,
                      "first_name":author.fname,
                      "last_name":author.lname,
                      "contact":author.contact,
                      "email":author.email,
                      "biography":author.biography,
                      "created_at":author.created_at,
                      "updated_at":author.updated_at,
                      "companies" : companies,
                    #   "books": books
                      }
                 }),HTTP_200_OK
        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR
        

        #UPDATING AUTHOR DETAILS
@authors.route('/edit/<int:author_id>', methods = ['PUT','PATCH']) #working with the route function
@jwt_required() # protects the route
def UpdateAuthorDetails(author_id):
        
        

        try:

            current_author = int(get_jwt_identity()) #returns the identity of a currently logged in author
            loggedinauthor = Author.query.filter_by(author_id = current_author).first()

            author = Author.query.filter_by(author_id=author_id).first()

            if not author:
                 return jsonify({
                      "Error":"Author not found"
                 }),HTTP_404_NOT_FOUND
            elif author.author_id!=current_author:
                 return jsonify({
                      "Error":"You are not authorized to update the author details"
                 }),HTTP_403_FORBIDDEN
            else:
                 fname = request.get_json().get("fname", author.fname)
                 lname = request.get_json().get("lname", author.lname)
                 contact = request.get_json().get("contact", author.contact)
                 email = request.get_json().get("email", author.email)
                 biography = request.get_json().get("biography", author.biography)

                 if "password" in request.json:
                      hashed_password = bcrypt.generate_password_hash(request.json.get("password"))
                      author.password = hashed_password


                 if email != author.email and Author.query.filter_by(email = email).first():
                      return jsonify({
                           "Error": "Email address already in use"
                      }),HTTP_409_CONFLICT
                 

                 if contact != author.contact and Author.query.filter_by(contact = contact).first():
                      return jsonify({
                           "Error": "contact already in use"
                      }),HTTP_409_CONFLICT

                 author.fname = fname
                 author.lname = lname
                 author.contact = contact
                 author.email = email
                 author.biography = biography

                 db.session.commit()

                 #get authors name
                 author_name = author.get_full_name()

                 return jsonify({
                      'message': author_name + "'s details have been updated successfully",
                      'author' : author.author_id,
                      'first_name' : author.fname,
                      'last_name' : author.lname,
                      'email' : author.email,
                      'contact': author.contact,
                      'biography': author.biography
                 })

                      


        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR
        

        #deleting an author
@authors.route('/delete/<int:author_id>', methods = ['DELETE']) #working with the route function
@jwt_required() # protects the route
def deleteauthor(author_id):
        
        

        try:

            current_author = int(get_jwt_identity()) #returns the identity of a currently logged in author
            loggedinauthor = Author.query.filter_by(author_id = current_author).first()
             
          # getting an author by id
            author = Author.query.filter_by(author_id=author_id).first()

            if not author:
                 return jsonify({
                      "Error":"Author not found"
                 }),HTTP_404_NOT_FOUND
            elif author.author_id!=current_author:
                 return jsonify({
                      "Error":"You are not authorized to update the author details"
                 }),HTTP_403_FORBIDDEN
            else:
                 
                 #delete associated companies
                 for company in author.companies:
                      db.session.delete(company)

               #    #delete associated books
               #   for book in author.books:
               #        db.session.delete(book)

                 db.session.delete(author)
                 db.session.commit()

                 return jsonify({
                      'message': "Author deleted successfully",
                 })

        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR    



# searching an author
@authors.get('/search')
@jwt_required()
def searchAuthors():

    try:

        search_query = request.args.get('query','')

        authors = Author.query.filter( or_ (Author.fname.ilike(f"%{search_query}%"),
                                       Author.lname.ilike(f"%{search_query}%"))).all()
        
        if len(authors) == 0:
             return jsonify({
                  'message':'No results found'
             }),HTTP_404_NOT_FOUND
        else:
             
             authors_data = []

        for author in authors:
            author_info = {
                "id" : author.author_id,
                "first_name" : author.fname,
                "last_name" : author.lname,
                "author_name" : author.get_full_name(),
                "email" : author.email,
                "contact" : author.contact,
                "created_at" : author.created_at,
               #  "companies": [],
               #  "books": []
                }
            
            authors_data.append(author_info)

        return jsonify({
            "Message": f"Authors with name {search_query} retrieved successfully",
            "total search": len(authors_data),
            "search_results":authors_data
        }),HTTP_200_OK #serializing the data enables us have a variable that can be converted to jsony easily
        
    except Exception as e:
        return  jsonify({
            "Error":str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR    
