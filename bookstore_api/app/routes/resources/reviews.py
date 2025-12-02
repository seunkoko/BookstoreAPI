from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from marshmallow import ValidationError

from bookstore_api.app.helpers import (
    RoleType, handle_errors, api_response, filter_and_sort_reviews,
    get_page_filters
)
from bookstore_api.app.schemas import ReviewSchema
from bookstore_api.app.models import Review, Book

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

DEFAULT_PER_PAGE = 10
DEFAULT_PAGE = 1


class ReviewListResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, book_id):
        """Fetching all reviews with optional filtering and pagination"""
        per_page, page = get_page_filters(request.args)
        if per_page is None or page is None:
            return handle_errors('Pagination parameters must be integers', 400)

        # Start with base query filtered by book_id
        try:
            query = Review.query.filter_by(book_id=int(book_id))
        except ValueError:
            return handle_errors('book_id must be an integer', 400)

        # Apply additional filters and sorting using helper function
        reviews = filter_and_sort_reviews(query, request.args)

        try:
            paginated_reviews = reviews.paginate(
                page=page, per_page=per_page, error_out=False)
            return api_response({
                'reviews': reviews_schema.dump(paginated_reviews.items),
                'total': paginated_reviews.total,
                'pages': paginated_reviews.pages,
                'current_page': paginated_reviews.page,
                'per_page': paginated_reviews.per_page
            }, message='Reviews fetched successfully', status_code=200)
        except Exception as e:
            current_app.logger.error(f"Error fetching reviews: {e}")
            return handle_errors('Error fetching reviews', 500, e)

    def post(self, book_id):
        """Creating a new review"""
        review_data = request.get_json(silent=True)
        try:
            validated_data = review_schema.load(review_data)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occurred during review creation: {e}")
            return handle_errors(
                'check that all required fields are present', 400, e)

        # Verify book exists
        Book.query.get_or_404(book_id, description='Book not found')

        # Set user_id from authenticated user
        current_user = get_current_user()
        validated_data['user_id'] = current_user.id
        validated_data['book_id'] = book_id

        try:
            new_review = Review(**validated_data)
            new_review.save()
        except Exception as e:
            current_app.logger.error(f"Error creating review: {e}")
            return handle_errors('Error creating review', 500, e)

        return api_response({
            'review': review_schema.dump(new_review)
        }, message='Review created successfully', status_code=201)


class ReviewResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, review_id):
        """Fetching a review by ID"""
        review = Review.query.get_or_404(review_id, description='Review not found')

        current_user = get_current_user()
        # Users can only view their own reviews, admins can view any
        if current_user.role.name != RoleType.ADMIN.value and review.user_id != current_user.id:
            return handle_errors('Unauthorized access', 403)

        return api_response({
            'review': review_schema.dump(review)
        }, message='Review fetched successfully', status_code=200)

    def put(self, review_id):
        """Updating a review by ID"""
        review_exists = Review.query.get_or_404(review_id, description='Review not found')

        current_user = get_current_user()
        # Only the review owner can update (not even admins)
        if review_exists.user_id != current_user.id:
            return handle_errors('Unauthorized access', 403)

        review_data = request.get_json(silent=True)
        try:
            validated_data = ReviewSchema(partial=True).load(review_data)
        except ValidationError as e:
            current_app.logger.error(f"Validation error occurred during review ({review_id}) update: {e}")
            return handle_errors('review update failure', 400, e)

        for key, value in validated_data.items():
            setattr(review_exists, key, value)

        try:
            review_exists.save()
        except Exception as e:
            current_app.logger.error(f"Error updating review with id {review_id}: {e}")
            return handle_errors('Error updating review', 500, e)

        return api_response({
            'review': review_schema.dump(review_exists)
        }, message='Review updated successfully', status_code=200)

    def delete(self, review_id):
        """Deleting a review by ID"""
        review = Review.query.get_or_404(review_id, description='Review not found')

        current_user = get_current_user()
        # Users can delete their own reviews, admins can delete any
        if current_user.role.name != RoleType.ADMIN.value and review.user_id != current_user.id:
            return handle_errors('Unauthorized access', 403)

        try:
            review.delete()
        except Exception as e:
            current_app.logger.error(f"Error deleting review with id {review_id}: {e}")
            return handle_errors('Error deleting review', 500, e)

        return api_response({}, message='Review deleted successfully', status_code=204)
