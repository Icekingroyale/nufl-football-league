from flask import Blueprint, request, jsonify, current_app, send_from_directory
import os
from werkzeug.utils import secure_filename

uploads_bp = Blueprint('uploads', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@uploads_bp.route('/upload', methods=['POST'])
def upload_file():
    from flask import session
    print('Session contents at upload:', dict(session))
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to prevent filename conflicts
        import time
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(time.time())}{ext}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        file.save(file_path)
        
        # Return the URL for the uploaded file
        from flask import url_for
        url = url_for('uploads.uploaded_file', filename=filename, _external=True)
        
        return jsonify({'url': url}), 201
    
    return jsonify({'error': 'File type not allowed'}), 400

@uploads_bp.route('/static/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename) 