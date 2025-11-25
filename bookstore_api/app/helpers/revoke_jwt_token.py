import os

from datetime import timedelta
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

ACCESS_EXPIRES = timedelta(hours=1)

def revoke_token(redis_db, jti: str):
    redis_db.setex(jti, os.getenv('JWT_ACCESS_TOKEN_EXPIRES', ACCESS_EXPIRES), 'true')
    return jsonify({"message": "Access token revoked"}), 200
