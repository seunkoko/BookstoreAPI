from flask import Blueprint
from flask_restful import Api

from .users import UserListResource
from .authors import AuthorListResource, AuthorResource
from .books import BookListResource, BookResource
from .book_categories import BookCategoryListResource, BookCategoryResource
from .reviews import ReviewListResource, ReviewResource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1/')
api = Api(api_bp)

# Add the resources to the Blueprint's API instance
api.add_resource(UserListResource, '/users', '/users/')
api.add_resource(AuthorListResource, '/authors', '/authors/')
api.add_resource(AuthorResource, '/authors/<int:author_id>', '/authors/<int:author_id>/')
api.add_resource(BookListResource, '/books', '/books/')
api.add_resource(BookResource, '/books/<int:book_id>', '/books/<int:book_id>/')
api.add_resource(BookCategoryListResource, '/book_categories', '/book_categories/')
api.add_resource(BookCategoryResource, '/book_categories/<int:category_id>', '/book_categories/<int:category_id>/')
api.add_resource(ReviewListResource, '/reviews/book/<int:book_id>', '/reviews/book/<int:book_id>/')
api.add_resource(ReviewResource, '/reviews/<int:review_id>', '/reviews/<int:review_id>/')
