from flask import Blueprint, request, jsonify

book_bp = Blueprint("book", __name__)

# Sample in-memory database
books = []

# Create a book
@book_bp.route("/", methods=["POST"])
def create_book():
    data = request.get_json()
    book = {"id": len(books) + 1, "title": data["title"], "author": data["author"]}
    books.append(book)
    return jsonify(book), 201

# Get all books
@book_bp.route("/", methods=["GET"])
def get_books():
    return jsonify(books)

# Get a single book by ID
@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else ("Book not found", 404)

# Update a book
@book_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        book.update(data)
        return jsonify(book)
    return ("Book not found", 404)

# Delete a book
@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return ("", 204)
