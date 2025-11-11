from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    return {'success': 'register success'}   

@auth_bp.route('/login', methods=['POST'])
def login():
    return {'success': 'login success'}   
