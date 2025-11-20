from flask import Blueprint
from flask_restful import Api

from .users import UserListResource
from .authors import AuthorListResource, AuthorResource

api_bp = Blueprint('api', __name__, url_prefix='/api/v1/')
api = Api(api_bp)

# Add the resources to the Blueprint's API instance
api.add_resource(UserListResource, '/users', '/users/')
api.add_resource(AuthorListResource, '/authors', '/authors/')
api.add_resource(AuthorResource, '/authors/<int:author_id>', '/authors/<int:author_id>/')
