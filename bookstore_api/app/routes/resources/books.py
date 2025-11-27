from flask_restful import Resource
from flask_jwt_extended import jwt_required

from bookstore_api.app.helpers import role_required, RoleType


class BookListResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self):
        pass  # Implementation for fetching list of books

    def post(self):
        pass  # Implementation for creating a new book


class BookResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self, book_id):
        pass  # Implementation for fetching a single book by ID

    def put(self, book_id):
        pass  # Implementation for updating a book by ID

    def delete(self, book_id):
        pass  # Implementation for deleting a book by ID
