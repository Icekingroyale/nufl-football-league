from flask import Blueprint, request, jsonify, current_app, session
import sqlite3
from datetime import datetime
from ..models import get_db_connection

news_bp = Blueprint('news', __name__, url_prefix='/api/news')

@news_bp.route('', methods=['GET'])
def get_all_news():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news ORDER BY created_at DESC")
    news_items = cursor.fetchall()
    conn.close()
    news_list = []
    for item in news_items:
        news_list.append({
            'id': item[0],
            'title': item[1],
            'content': item[2],
            'author': item[3],
            'category': item[4],
            'image_url': item[5],
            'published': bool(item[6]),
            'created_at': item[7]
        })
    return jsonify(news_list)

@news_bp.route('/<int:news_id>', methods=['GET'])
def get_news(news_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (news_id,))
    news_item = cursor.fetchone()
    conn.close()
    if news_item:
        return jsonify({
            'id': news_item[0],
            'title': news_item[1],
            'content': news_item[2],
            'author': news_item[3],
            'category': news_item[4],
            'image_url': news_item[5],
            'published': bool(news_item[6]),
            'created_at': news_item[7]
        })
    else:
        return jsonify({'error': 'News article not found'}), 404

@news_bp.route('', methods=['POST'])
def create_news():
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO news (title, content, author, category, image_url, published, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('title'),
            data.get('content'),
            data.get('author'),
            data.get('category'),
            data.get('image_url'),
            data.get('published', True),
            datetime.now().isoformat()
        ))
        conn.commit()
        news_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'News article created successfully', 'id': news_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@news_bp.route('/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE news 
            SET title = ?, content = ?, author = ?, category = ?, image_url = ?, published = ?
            WHERE id = ?
        """, (
            data.get('title'),
            data.get('content'),
            data.get('author'),
            data.get('category'),
            data.get('image_url'),
            data.get('published'),
            news_id
        ))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'News article not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'News article updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@news_bp.route('/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'News article not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'News article deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500 