from flask import current_app, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from bookstore_api.app.helpers import role_required, RoleType, api_response, handle_errors
from bookstore_api.app.schemas import AuthorSchema
from bookstore_api.app.models import Author

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


class AuthorListResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self):
        try:
            return api_response({
                'authors': authors_schema.dump(Author.query.all())
            }, message='Authors fetched successfully', status_code=200)
        except Exception as e:
            current_app.logger.error(f"Error fetching authors: {e}")
            return handle_errors('Error fetching authors', 500, e)
    
    def post(self):
        author_data = request.get_json(silent=True)
        try:
            validated_data = author_schema.load(author_data)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occured during author creation: {e}")
            return handle_errors('author creation failure', 400, e)
    
        author_exists = Author.query.filter_by(name=validated_data['name'].lower()).one_or_none()
        if author_exists:
            return handle_errors(f'author with name ({validated_data["name"]}) already exists', 400)
        
        try:
            validated_data['name'] = validated_data['name'].lower()
            new_author = Author(**validated_data)
            new_author.save()
        except Exception as e:
            current_app.logger.error(f"Error creating author: {e}")
            return handle_errors('Error creating author', 500, e)
        
        return api_response({
            'author': author_schema.dump(new_author)
        }, message='Author created successfully', status_code=201)


class AuthorResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self, author_id):
        author = Author.query.get_or_404(author_id, description='Author not found')
        
        return api_response({
            'author': author_schema.dump(author)
        }, message='Author fetched successfully', status_code=200)
    
    def put(self, author_id):
        author_data = request.get_json(silent=True)
        author_schema = AuthorSchema(partial=True, exclude=['books'])

        try:
            validated_data = author_schema.load(author_data)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occured during author update: {e}")
            return handle_errors('author update failure', 400, e)

        author = Author.query.get_or_404(author_id, description='Author not found')
        for key, value in validated_data.items():
            # Use built-in Python function setattr() to update the attribute by name
            setattr(author, key, value)
    
        try:
            author.save()
        except Exception as e:
            current_app.logger.error(f"Error updating author: {e}")
            return handle_errors('Error updating author', 500, e)
        
        return api_response({
            'author': author_schema.dump(author)
        }, message='Author updated successfully', status_code=200)
    
    def delete(self, author_id):
        author = Author.query.get_or_404(author_id, description='Author not found')
    
        try:
            author.delete()
        except Exception as e:
            current_app.logger.error(f"Error deleting author: {e}")
            return handle_errors('Error deleting author', 500, e)
        
        return api_response({}, message='Author deleted successfully', status_code=204)
