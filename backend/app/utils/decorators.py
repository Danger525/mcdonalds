from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != required_role:
                return jsonify(msg='Admins only!'), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    return role_required('admin')(fn)

def staff_required(fn):
    # Example: Allow staff or admin
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') not in ['admin', 'manager', 'kitchen']:
             return jsonify(msg='Staff only!'), 403
        return fn(*args, **kwargs)
    return wrapper
