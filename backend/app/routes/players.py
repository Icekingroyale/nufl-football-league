from flask import Blueprint, request, jsonify, current_app, session
import sqlite3
from ..models import get_db_connection

players_bp = Blueprint('players', __name__, url_prefix='/api')

@players_bp.route('/players', methods=['GET'])
def get_players():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.team_id, t.name as team_name, p.position, p.jersey_number, p.age, p.nationality, p.height, p.weight, p.photo_url
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        ORDER BY t.name, p.name
    """)
    players = cursor.fetchall()
    conn.close()
    players_list = []
    for player in players:
        players_list.append({
            'id': player[0],
            'name': player[1],
            'team_id': player[2],
            'team_name': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'nationality': player[7],
            'height': player[8],
            'weight': player[9],
            'photo_url': player[10]
        })
    return jsonify(players_list)

@players_bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.team_id, t.name as team_name, p.position, p.jersey_number, p.age, p.nationality, p.height, p.weight, p.photo_url
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        WHERE p.id = ?
    """, (player_id,))
    player = cursor.fetchone()
    conn.close()
    if player:
        return jsonify({
            'id': player[0],
            'name': player[1],
            'team_id': player[2],
            'team_name': player[3],
            'position': player[4],
            'jersey_number': player[5],
            'age': player[6],
            'nationality': player[7],
            'height': player[8],
            'weight': player[9],
            'photo_url': player[10]
        })
    else:
        return jsonify({'error': 'Player not found'}), 404

@players_bp.route('/players', methods=['POST'])
def create_player():
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO players (name, team_id, position, jersey_number, age, nationality, height, weight, photo_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('name'),
            data.get('team_id'),
            data.get('position'),
            data.get('jersey_number'),
            data.get('age'),
            data.get('nationality'),
            data.get('height'),
            data.get('weight'),
            data.get('photo_url')
        ))
        conn.commit()
        player_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Player created successfully', 'id': player_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@players_bp.route('/players/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE players 
            SET name = ?, team_id = ?, position = ?, jersey_number = ?, age = ?, nationality = ?, height = ?, weight = ?, photo_url = ?
            WHERE id = ?
        """, (
            data.get('name'),
            data.get('team_id'),
            data.get('position'),
            data.get('jersey_number'),
            data.get('age'),
            data.get('nationality'),
            data.get('height'),
            data.get('weight'),
            data.get('photo_url'),
            player_id
        ))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Player not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Player updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@players_bp.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Player not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Player deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500 