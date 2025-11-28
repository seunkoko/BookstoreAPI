from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from bookstore_api.app.helpers import role_required, RoleType, handle_errors, api_response
from bookstore_api.app.schemas import BookSchema
from bookstore_api.app.models import Book, Author, BookCategory
from bookstore_api.app.services import upload_photo_to_s3

book_schema = BookSchema()
books_schema = BookSchema(many=True)

class BookListResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self):
        pass  # Implementation for fetching list of books

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
        pass  # Implementation for fetching a single book by ID

    def put(self, book_id):
        pass  # Implementation for updating a book by ID

    def delete(self, book_id):
        pass  # Implementation for deleting a book by ID
