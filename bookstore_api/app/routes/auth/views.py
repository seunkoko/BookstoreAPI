from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import redis

from bookstore_api.app.helpers import (
    handle_errors, api_response, RoleType, revoke_token, is_valid_email_format, is_strong_password
)
from bookstore_api.app.schemas.user_schema import UserSchema
from bookstore_api.app.models import User, Role
from bookstore_api.app.extensions import jwt

### Initialize Redis connection
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    # handle user registration
    user_schema = UserSchema()

    try:
        validated_data = user_schema.load(request.get_json(silent=True))
    except ValidationError as e:
        current_app.logger.error(f"Validation error occured during registration: {e}")
        return handle_errors('register failure', 400, e)

    if not is_valid_email_format(validated_data['email']):
        return handle_errors('invalid email format', 400)

    if not is_strong_password(validated_data['password']):
        return handle_errors('weak password', 400)

    user_exists = User.query.filter_by(email=validated_data['email']).one_or_none()
    if user_exists:
        return handle_errors('user already exists', 400)

    role = Role.query.filter_by(name=RoleType.USER.value).one_or_none()
    if not role:
        current_app.logger.error(f"Role name not found: {RoleType.USER.value} when creating user")
        return handle_errors('role not found', 400)

    hashed_password = generate_password_hash(validated_data['password'])
    new_user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        password_hash=hashed_password,
        role_id=role.id
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
            'access_token': create_access_token(identity=str(user.id)),
            'user': UserSchema().dump(user)
        },
        message="Login successful",
        status_code=200
    )

@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    return revoke_token(redis_db, get_jwt()["jti"])

@auth_bp.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access_token():
    return revoke_token(redis_db, get_jwt()["jti"])

@auth_bp.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_refresh_token():
    return revoke_token(redis_db, get_jwt()["jti"])

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    return redis_db.get(jti) is not None

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # 'jwt_data' is a dictionary containing the claims (payload) of the token
    # The identity is stored under the key defined by JWT_IDENTITY_CLAIM (default: 'sub')
    identity = jwt_data["sub"]

    return User.query.get(int(identity))
