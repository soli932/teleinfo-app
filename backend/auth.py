from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps

auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

# Usuarios predefinidos (en producción usar una base de datos)
users = {
    'admin': {
        'password': 'Adminpw1',  # En producción usar hash de contraseñas
        'role': 'admin'
    },
    'editor': {
        'password': 'Sca.123',
        'role': 'editor'
    }
}

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Usuario y contraseña requeridos'}), 400
        
        user = users.get(username)
        if user and user['password'] == password:
            access_token = create_access_token(identity=username, additional_claims={'role': user['role']})
            return jsonify({
                'token': access_token,
                'user': {
                    'username': username,
                    'role': user['role']
                }
            })
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        return jsonify({
            'username': current_user,
            'role': claims['role']
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Decorator para verificar roles
def requires_roles(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] not in roles:
                return jsonify({'message': 'Acceso no autorizado'}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper
