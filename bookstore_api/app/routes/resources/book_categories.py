from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from bookstore_api.app.helpers import role_required, RoleType, handle_errors, api_response
from bookstore_api.app.schemas import BookCategorySchema
from bookstore_api.app.models import BookCategory

category_schema = BookCategorySchema(exclude=['books'])
categories_schema = BookCategorySchema(many=True, exclude=['books'])


class BookCategoryListResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def get(self):
        """Fetching all book categories"""
        try:
            return api_response({
                'book_categories': categories_schema.dump(BookCategory.query.order_by(BookCategory.name).all())
            }, message='Book categories fetched successfully', status_code=200)
        except Exception as e:
            current_app.logger.error(f"Error fetching book categories: {e}")
            return handle_errors('Error fetching book categories', 500, e)

    def post(self):
        """Creating a new book category"""
        category_data = request.get_json(silent=True)
    
        try:
            validated_data = category_schema.load(category_data)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occured during book category creation: {e}")
            return handle_errors('book category creation failure', 400, e)
        
        category_exists = BookCategory.query.filter_by(name=validated_data['name'].lower()).one_or_none()
        if category_exists:
            return handle_errors(f'book category with name ({validated_data["name"]}) already exists', 400)

        try:
            validated_data['name'] = validated_data['name'].lower()
            new_category = BookCategory(**validated_data)
            new_category.save()
        except Exception as e:
            current_app.logger.error(f"Error creating book category: {e}")
            return handle_errors('Error creating book category', 500, e)
        
        return api_response({
            'book_category': category_schema.dump(new_category)
        }, message='Book category created successfully', status_code=201)


class BookCategoryResource(Resource):
    method_decorators = [role_required(RoleType.ADMIN.value), jwt_required()]

    def put(self, category_id):
        """Updating a book category by ID"""
        category_schema = BookCategorySchema(partial=True, exclude=['books'])

        try:
            validated_data = category_schema.load(request.get_json(silent=True))
        except ValidationError as e:
            current_app.logger.error(f"Validation error occured during book category ({category_id}) update: {e}")
            return handle_errors('book category update failure', 400, e)

        category = BookCategory.query.get_or_404(category_id, description='Book category not found')
        for key, value in validated_data.items():
            setattr(category, key, value)

        try:
            category.save()
        except Exception as e:
            current_app.logger.error(f"Error updating book category with id {category_id}: {e}")
            return handle_errors('Error updating book category', 500, e)
        
        return api_response({
            'book_category': category_schema.dump(category)
        }, message='Book category updated successfully', status_code=200)

    def delete(self, category_id):
        """Deleting a book category by ID"""
        category = BookCategory.query.get_or_404(category_id, description='Book category not found')

        try:
            category.delete()
        except Exception as e:
            current_app.logger.error(f"Error deleting book category with id {category_id}: {e}")
            return handle_errors('Error deleting book category', 500, e)
        
        return api_response({}, message='Book category deleted successfully', status_code=204)
