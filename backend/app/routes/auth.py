from flask import Blueprint, request, jsonify, session
import hashlib
import time

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    print(f"Login attempt - Method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request data: {request.get_data()}")
    
    try:
        data = request.get_json()
        print(f"Parsed JSON data: {data}")
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        print(f"Login attempt for username: {username}")
        
        if username == 'admin' and password == 'admin123':
            # Generate a simple token
            token = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
            
            # Store token in session
            session['auth_token'] = token
            session['username'] = username
            
            print(f"Login successful, token generated: {token}")
            print(f"Session after login: {dict(session)}")
            
            response = jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {'username': username},
                'token': token
            })
            
            # Set session cookie
            session.permanent = True
            
            return response
        else:
            print(f"Login failed - Invalid credentials for username: {username}")
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    print("Logout request received")
    session.clear()
    print("Logout successful, session cleared")
    return jsonify({'success': True, 'message': 'Logout successful'})

@auth_bp.route('/check_auth')
def check_auth():
    print(f"Check auth request - Session contents: {dict(session)}")
    if 'auth_token' in session:
        return jsonify({
            'authenticated': True,
            'user': {'username': session.get('username')}
        })
    else:
        return jsonify({'authenticated': False}), 401 