from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_403_FORBIDDEN
import validators
from app.models.company_model import Company
from app.models import author_model
from app.models.author_model import Author
from app.models import book_model
from app.models.book_model import Book
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token

#book blueprint
books = Blueprint('books', __name__,
                        url_prefix='/api/v1/books') #creating a new object


#creating books
@books.route("/create", methods = ['POST'])
@jwt_required()
def create_book():

    #storing request values
    data = request.get_json()
    title = data.get("title")
    pages = data.get("pages")
    price = data.get("price")
    genre = data.get("genre")
    isbn = data.get("isbn")
    image = data.get("image")
    description = data.get("description")
    publisher = data.get("publisher")
    price_unit = data.get("price_unit")
    publication_date = data.get("publication_date")
    company_id = data.get("company_id")
    author_id = get_jwt_identity()


    #validations of the incoming requests
    if not title or not pages or not price or not publisher or not genre or not price_unit or not company_id or not publication_date or not description or not isbn or not image:
        return jsonify({"Error":"All fields are required"}),HTTP_400_BAD_REQUEST

    if Book.query.filter_by(title=title,author_id = author_id).first() is not None:
        return jsonify({"Error":"Book with this title and author_id already exists"}),HTTP_409_CONFLICT
    
    if Book.query.filter_by(isbn=isbn).first() is not None:
        return jsonify({"Error":"Book isbn already in use"}),HTTP_409_CONFLICT
    
    try:

        #creating a new book
        new_book = Book(title=title,publication_date=publication_date,author_id=author_id,price=price,pages=pages,price_unit=price_unit,genre=genre,company_id=company_id,isbn=isbn,image=image,publisher=publisher,description=description)
        db.session.add(new_book)
        db.session.commit()


        return jsonify({"Message":title + "has been successfully created ",
                        "book":{
                            "id":new_book.book_ID,
                            "title":new_book.title,
                            "price":new_book.price,
                            "pages":new_book.pages,
                            "genre":new_book.genre,
                            "publisher":new_book.publisher,
                            "description":new_book.description,
                            "price_unit":new_book.price_unit,
                            "publication_date":new_book.publication_date,
                            "created_at":new_book.created_at,
                            "company": {
                                "id":new_book.company.company_id,
                                "name":new_book.company.name,
                                "location":new_book.company.location,
                                "contact":new_book.company.contact,
                                "email":new_book.company.email,
                                "created_at":new_book.company.created_at
                            },
                            "author" : {
                                "id" : new_book.author.author_id,
                                "first_name" : new_book.author.fname,
                                "last_name" : new_book.author.lname,
                                "author_name" : new_book.author.get_full_name(),
                                "email" : new_book.author.email,
                                "contact" : new_book.author.contact,
                                "created_at" : new_book.author.created_at,
                            }

                        }
                        
                        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
#getting all books
@books.get('/')
@jwt_required()
def getallbooks():


    try:

        all_books = Book.query.all()


        books_data = []

        for book in all_books:
            book_info = {
                "id":book.book_ID,
                "title":book.title,
                "price":book.price,
                "pages":book.pages,
                "genre":book.genre,
                "publisher":book.publisher,
                "description":book.description,
                "price_unit":book.price_unit,
                "publication_date":book.publication_date,
                "created_at":book.created_at,
                "company": {
                        "id":book.company.company_id,
                        "name":book.company.name,
                        "location":book.company.location,
                        "contact":book.company.contact,
                        "email":book.company.email,
                        "created_at":book.company.created_at
                },


                }
            
            books_data.append(book_info)

        return jsonify({
            "Message": "All books retrieved successfully",
            "total books": len(books_data),
            "books":books_data
        }),HTTP_200_OK #serializing the data enables us have a variable that can be converted to jsony easily
        
    except Exception as e:
        return  jsonify({
            "Error":str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    



#getting a book by id
@books.get('/book/<int:book_id>')
@jwt_required()
def getbook(book_id):
        
        

        try:
            book = Book.query.filter_by(book_ID = book_id).first()

            if not book:
                 return jsonify({
                      "Error":"Book not found"
                 }),HTTP_404_NOT_FOUND
            return jsonify({
                 "Message": "Book details retrieved successfully",
                 "book":{
                            "id":book.book_ID,
                            "title":book.title,
                            "price":book.price,
                            "pages":book.pages,
                            "genre":book.genre,
                            "publisher":book.publisher,
                            "description":book.description,
                            "price_unit":book.price_unit,
                            "publication_date":book.publication_date,
                            "created_at":book.created_at,
                            "company": {
                                "id":book.company.company_id,
                                "name":book.company.name,
                                "location":book.company.location,
                                "contact":book.company.contact,
                                "email":book.company.email,
                                "created_at":book.company.created_at
                            },
                            "author" : {
                                "id" : book.author.author_id,
                                "first_name" : book.author.fname,
                                "last_name" : book.author.lname,
                                "author_name" : book.author.get_full_name(),
                                "email" : book.author.email,
                                "contact" : book.author.contact,
                                "created_at" : book.author.created_at,
                            }
                        }
                 }),HTTP_200_OK
        

        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR
    

# updating book details
@books.route('/edit/<int:book_id>', methods = ['PUT','PATCH']) #working with the route function
@jwt_required() # protects the route
def UpdatebookDetails(book_id):
        
        

        try:

            current_author = int(get_jwt_identity()) #returns the identity of a currently logged in author
            loggedinauthor = Author.query.filter_by(author_id = current_author).first()

            # get book by id
            book = Book.query.filter_by(book_ID=book_id).first()

            if not book:
                 return jsonify({
                      "Error":"book not found"
                 }),HTTP_404_NOT_FOUND
            
            elif book.author_id!=current_author:
                 return jsonify({
                      "Error":"You are not authorized to update the book details"
                 }),HTTP_403_FORBIDDEN
            
            else:
                 # storing request data
                 title = request.get_json().get("title", book.title)
                 price = request.get_json().get("price", book.price)
                 pages = request.get_json().get("pages", book.pages)
                 genre = request.get_json().get("genre", book.genre)
                 isbn = request.get_json().get("isbn", book.isbn)
                 image = request.get_json().get("image", book.image)
                 description = request.get_json().get("description", book.description)
                 price_unit = request.get_json().get("price_unit", book.price_unit)
                 company_id = request.get_json().get("company_id", book.company_id)

                 

                 if isbn != book.isbn and Book.query.filter_by(isbn = isbn).first():
                      return jsonify({
                           "Error": "ISBN already in use"
                      }),HTTP_409_CONFLICT
                 
                 if title != book.title and Book.query.filter_by(title = title,author_id=current_author).first():
                      return jsonify({
                           "Error": "Book title already in use"
                      }),HTTP_409_CONFLICT

                 book.title = title
                 book.price = price
                 book.price_unit = price_unit
                 book.genre = genre
                 book.image = image
                 book.pages = pages
                 book.description = description
                 book.company_id = company_id

                 db.session.commit()



                 return jsonify({
                      'message': title + "'s details have been updated successfully",
                      'book' :{
                            "id":book.book_ID,
                            "title":book.title,
                            "price":book.price,
                            "pages":book.pages,
                            "genre":book.genre,
                            "publisher":book.publisher,
                            "description":book.description,
                            "price_unit":book.price_unit,
                            "publication_date":book.publication_date,
                            "created_at":book.created_at,
                            "company": {
                                "id":book.company.company_id,
                                "name":book.company.name,
                                "location":book.company.location,
                                "contact":book.company.contact,
                                "email":book.company.email,
                                "created_at":book.company.created_at
                            },
                            "author" : {
                                "id" : book.author.author_id,
                                "first_name" : book.author.fname,
                                "last_name" : book.author.lname,
                                "author_name" : book.author.get_full_name(),
                                "email" : book.author.email,
                                "contact" : book.author.contact,
                                "created_at" : book.author.created_at,
                            }
                        }
                 })
            
        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR


# deleting a book
@books.route('/delete/<int:book_id>', methods = ['DELETE']) #working with the route function
@jwt_required() # protects the route
def deletebook(book_id):
        
        

        try:

            current_author = int(get_jwt_identity()) #returns the identity of a currently logged in author
            loggedinauthor = Author.query.filter_by(author_id = current_author).first()
             
          # getting a company by id
            book = Book.query.filter_by(book_ID=book_id).first()

            if not book:
                 return jsonify({
                      "Error":"Book not found"
                 }),HTTP_404_NOT_FOUND
            
            elif book.author_id!=current_author:
                 return jsonify({
                      "Error":"You are not authorized to update the author details"
                 }),HTTP_403_FORBIDDEN
            
            else:
                 

                 db.session.delete(book)
                 db.session.commit()

                 return jsonify({
                      'message': "Book deleted successfully",
                 })

        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR      
