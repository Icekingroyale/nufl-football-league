from flask import Blueprint, request, jsonify, current_app, session
import sqlite3
from datetime import datetime
from ..models import get_db_connection

news_bp = Blueprint('news', __name__, url_prefix='/api')

@news_bp.route('/news', methods=['GET'])
def get_news():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, content, author, category, image_url, published, created_at
        FROM news
        WHERE published = 1
        ORDER BY created_at DESC
    """)
    news = cursor.fetchall()
    conn.close()
    news_list = []
    for article in news:
        news_list.append({
            'id': article[0],
            'title': article[1],
            'content': article[2],
            'author': article[3],
            'category': article[4],
            'image_url': article[5],
            'published': article[6],
            'created_at': article[7]
        })
    return jsonify(news_list)

@news_bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_article(news_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, content, author, category, image_url, published, created_at
        FROM news
        WHERE id = ? AND published = 1
    """, (news_id,))
    article = cursor.fetchone()
    conn.close()
    if article:
        return jsonify({
            'id': article[0],
            'title': article[1],
            'content': article[2],
            'author': article[3],
            'category': article[4],
            'image_url': article[5],
            'published': article[6],
            'created_at': article[7]
        })
    else:
        return jsonify({'error': 'News article not found'}), 404

@news_bp.route('/news', methods=['POST'])
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
            data.get('author', 'Admin'),
            data.get('category', 'General'),
            data.get('image_url'),
            data.get('published', 1),
            datetime.now().isoformat()
        ))
        conn.commit()
        news_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'News article created successfully', 'id': news_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@news_bp.route('/news/<int:news_id>', methods=['PUT'])
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
            data.get('published', 1),
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

@news_bp.route('/news/<int:news_id>', methods=['DELETE'])
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