from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_200_OK
from app.models.book_model import Book  # Import the Book model
from app.extensions import db
from datetime import datetime

# Book blueprint
book = Blueprint('book', __name__, url_prefix='/api/v1/books')

# Create a new book
@book.route('/register', methods=['POST'])
def create_book():
    data = request.json
    title = data.get('title')
    pages = data.get('pages')
    price = data.get('price')
    description = data.get('description')
    authorsname = data.get('authorsname')
    publishersname = data.get('publishersname')
    publicationdate = data.get('publicationdate')
    no_of_pages = data.get('no_of_pages')

    # Validate the incoming request
    if not title or not pages or not price or not description or not authorsname or not publishersname or not publicationdate or not no_of_pages:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    try:
        # Create a new book
        new_book = Book(
            title=title,
            pages=pages,
            price=price,
            description=description,
            authorsname=authorsname,
            publishersname=publishersname,
            publicationdate=publicationdate,
            no_of_pages=no_of_pages
        )
        db.session.add(new_book)
        db.session.commit()

        return jsonify({
            "message": "Book created successfully",
            "book": {
                "id": new_book.id,
                "title": new_book.title,
                "pages": new_book.pages,
                "price": new_book.price,
                "description": new_book.description,
                "authorsname": new_book.authorsname,
                "publishersname": new_book.publishersname,
                "publicationdate": new_book.publicationdate,
                "no_of_pages": new_book.no_of_pages,
                "created_at": new_book.created_at,
                "updated_at": new_book.updated_at
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get all books
@book.route('/', methods=['POST'])
def get_all_books():
    try:
        books = Book.query.all()
        books_list = [{
            "id": book.id,
            "title": book.title,
            "pages": book.pages,
            "price": book.price,
            "description": book.description,
            "authorsname": book.authorsname,
            "publishersname": book.publishersname,
            "publicationdate": book.publicationdate,
            "no_of_pages": book.no_of_pages,
            "created_at": book.created_at,
            "updated_at": book.updated_at
        } for book in books]

        return jsonify({
            "message": "Books retrieved successfully",
            "books": books_list
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get a single book by ID
@book.route('/login', methods=['POST'])
def get_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "message": "Book retrieved successfully",
            "book": {
                "id": book.id,
                "title": book.title,
                "pages": book.pages,
                "price": book.price,
                "description": book.description,
                "authorsname": book.authorsname,
                "publishersname": book.publishersname,
                "publicationdate": book.publicationdate,
                "no_of_pages": book.no_of_pages,
                "created_at": book.created_at,
                "updated_at": book.updated_at
            }
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR