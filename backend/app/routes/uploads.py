from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory
import os
from ..utils import allowed_file

uploads_bp = Blueprint('uploads', __name__, url_prefix='/api')

@uploads_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename  # You may want to use secure_filename in production
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        url = url_for('uploads.uploaded_file', filename=filename, _external=True)
        return jsonify({'url': url}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@uploads_bp.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename) 