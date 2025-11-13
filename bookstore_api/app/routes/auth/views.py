from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from bookstore_api.app.helpers import handle_errors, api_response
from bookstore_api.app.schemas.user_schema import UserSchema
from bookstore_api.app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    # handle user registration
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
    # handle user login
    login_data = request.get_json(silent=True)
    if not login_data or 'email' not in login_data or 'password' not in login_data:
        return handle_errors('please provide credentials to login', 400)
    
    user = User.query.filter_by(email=login_data['email']).one_or_none()
    if not user or not check_password_hash(user.password_hash, login_data['password']):
        return handle_errors(
            'invalid email or password, please check your credentials to login again',
            400
        )
    
    return api_response(
        data={
            'access_token': create_access_token(identity=user.id),
            'user': UserSchema().dump(user)
        },
        message="Login successful",
        status_code=200
    )
