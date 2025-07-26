from flask import Blueprint, request, jsonify, session
import hashlib
import time

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'admin123':
        # Generate a simple token
        token = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
        
        # Store token in session
        session['auth_token'] = token
        session['username'] = username
        
        print(f"Login successful, token generated: {token}")  # Debug print
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {'username': username},
            'token': token
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    print("Logout successful, session cleared")  # Debug print
    return jsonify({'success': True, 'message': 'Logout successful'})

@auth_bp.route('/check_auth')
def check_auth():
    print(f"Session contents: {dict(session)}")  # Debug print
    if 'auth_token' in session:
        return jsonify({
            'authenticated': True,
            'user': {'username': session.get('username')}
        })
    else:
        return jsonify({'authenticated': False}), 401 