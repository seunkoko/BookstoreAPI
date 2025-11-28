from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from bookstore_api.app.helpers import (
    role_required, RoleType, handle_errors, api_response,
    search_filter_and_sort_books
)
from bookstore_api.app.schemas import BookSchema
from bookstore_api.app.models import Book, Author, BookCategory
from bookstore_api.app.services import upload_photo_to_s3, delete_photo_from_s3

book_schema = BookSchema()
books_schema = BookSchema(many=True)

DEFAULT_PER_PAGE = 10
DEFAULT_PAGE = 1

class BookListResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self):
        """Fetching all books with pagination"""
        try:
            per_page = int(request.args.get('per_page', DEFAULT_PER_PAGE))
            page = int(request.args.get('page', DEFAULT_PAGE))
        except ValueError as e:
            current_app.logger.error(f"Pagination parameters must be integers: {e}")
            return handle_errors('Pagination parameters must be integers', 400, e)

        books = search_filter_and_sort_books(Book.query, request.args)
        try:
            paginated_books = books.paginate(
                page=page, per_page=per_page, error_out=False)
            return api_response({
                'books': books_schema.dump(paginated_books.items),
                'total': paginated_books.total,
                'pages': paginated_books.pages,
                'current_page': paginated_books.page,
                'per_page': paginated_books.per_page
            }, message='Books fetched successfully', status_code=200)
        except Exception as e:
            current_app.logger.error(f"Error fetching books: {e}")
            return handle_errors('Error fetching books', 500, e)

    def post(self):
        """Creating a new book"""
        try:
            validated_data = book_schema.load(request.form)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occured during book creation: {e}")
            return handle_errors(
                'check that all required fields are present', 400, e)

        Author.query.get_or_404(validated_data['author_id'], description='Author not found')
        if validated_data.get('category_id'):
            BookCategory.query.get(validated_data['category_id'], description='Book category not found')

        try:
            new_book = Book(**validated_data)
            new_book.save()
        except Exception as e:
            current_app.logger.error(f"Error creating book: {e}")
            return handle_errors('Error creating book', 500, e)

        cover_image = request.files.get('cover_image')
        if cover_image and cover_image.filename != '':
            # TODO: Can use celery task for handling file uploads in background if needed
            validated_data['cover_image_url'], validated_data['cover_image_s3_key'] = upload_photo_to_s3(
                cover_image, cover_image.filename)

        try:
            setattr(new_book, 'cover_image_url', validated_data.get('cover_image_url'))
            setattr(new_book, 'cover_image_s3_key', validated_data.get('cover_image_s3_key'))
            new_book.save()
        except Exception as e:
            current_app.logger.error(f"Error updating book with cover image info: {e}")
            return handle_errors('Error updating book with cover image info', 500, e)

        return api_response({
            'book': book_schema.dump(new_book)
        }, message='Book created successfully', status_code=201)


class BookResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self, book_id):
        """Fetching a book by ID"""
        book = Book.query.get_or_404(book_id, description='Book not found')
        return api_response({
            'book': book_schema.dump(book)
        }, message='Book fetched successfully', status_code=200)

    def put(self, book_id):
        """Updating a book by ID"""
        book_exists = Book.query.get_or_404(book_id, description='Book not found')
        try:
            validated_data = BookSchema(partial=True).load(request.form)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occured during book ({book_id}) update: {e}")
            return handle_errors('book update failure', 400, e)

        if validated_data.get('author_id'):
            Author.query.get_or_404(validated_data['author_id'], description='Author not found')
        if validated_data.get('category_id'):
            BookCategory.query.get_or_404(
                validated_data['category_id'], description='Book category not found')

        # TODO: Can use celery task for handling file uploads in background if needed
        cover_image = request.files.get('cover_image')
        if cover_image and cover_image.filename != '':
            # Delete old cover image from S3 if exists
            if book_exists.cover_image_s3_key:
                delete_photo_from_s3(book_exists.cover_image_s3_key)
            # Upload new cover image to S3
            validated_data['cover_image_url'], validated_data['cover_image_s3_key'] = upload_photo_to_s3(
                cover_image, cover_image.filename)

        for key, value in validated_data.items():
            setattr(book_exists, key, value)
        try:
            book_exists.save()
        except Exception as e:
            current_app.logger.error(f"Error updating book with id {book_id}: {e}")
            return handle_errors('Error updating book', 500, e)

        return api_response({
            'book': book_schema.dump(book_exists)
        }, message='Book updated successfully', status_code=200)

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id, description='Book not found')

        try:
            # Delete cover image from S3 if exists
            if book.cover_image_s3_key:
                delete_photo_from_s3(book.cover_image_s3_key)
            book.delete()
        except Exception as e:
            current_app.logger.error(f"Error deleting book with id {book_id}: {e}")
            return handle_errors('Error deleting book', 500, e)

        return api_response({}, message='Book deleted successfully', status_code=204)
