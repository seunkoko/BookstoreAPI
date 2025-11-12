from flask import Blueprint, request, current_app
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash

from bookstore_api.app.helpers import handle_errors, api_response
from bookstore_api.app.schemas.user_schema import UserSchema
from bookstore_api.app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    # handle user registration
    """
    - get data from request
    - validate data (schema, password, check if user exists)
    - create user 
    - return success
    """
    user_schema = UserSchema()

    try:
        validated_data = user_schema.load(request.get_json(silent=True))
    except ValidationError as e:
        current_app.logger.error(f"Validation error occured during registration: {e}")
        return handle_errors('register failure', 400)
    
    user_exists = User.query.filter_by(email=validated_data['email']).one_or_none()
    if user_exists:
        return handle_errors('user already exists', 400)
    
    hashed_password = generate_password_hash(validated_data['password'])
    new_user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        password_hash=hashed_password
    )

    try:
        new_user.save()
    except Exception as e:
        current_app.logger.error(f"Error creating new user: {e}")
        return handle_errors(
            "Error creating new user. Please check your data and try again",
            500,
            e
        )
    
    return api_response(
        data=user_schema.dump(new_user),
        message="User created successfully",
        status_code=201
    )  

@auth_bp.route('/login', methods=['POST'])
def login():
    return handle_errors('login failure', 401)
