from . import auth_bp
from flask import request, jsonify
from app import db, jwt, limiter
from app.models import User, Role
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,  get_jwt

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400
        
    # Default to Customer role
    role = Role.CUSTOMER
    if 'role' in data:
        try:
            role = Role(data['role'])
        except ValueError:
            return jsonify({"message": "Invalid role"}), 400

    new_user = User(username=data['username'], role=role)
    if 'email' in data:
        new_user.email = data['email']
        
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    print(f"Login attempt for: {data.get('username')}")
    
    user = User.query.filter_by(username=data['username']).first()
    print(f"User found: {user}")
    
    if user:
        is_valid = user.check_password(data['password'])
        print(f"Password check result for {user.username}: {is_valid}")
        if is_valid:
            # Create tokens
            access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role.value})
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return jsonify({
                "access_token": access_token, 
                "refresh_token": refresh_token,
                "role": user.role.value,
                "username": user.username
            }), 200
        else:
             print("Matches hash:", user.password_hash)
        
    return jsonify({"message": "Invalid credentials"}), 401



@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    new_access_token = create_access_token(identity=current_user_id, additional_claims={"role": user.role.value})
    return jsonify(access_token=new_access_token), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Because we are using JWT tokens (stateless), "logout" is effectively handled client-side 
    # by discarding the token. However, if we move to blacklist/blocklist later, we'd add it here.
    return jsonify({"message": "Successfully logged out"}), 200

