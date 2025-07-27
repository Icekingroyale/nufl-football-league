from flask import Blueprint, request, jsonify, current_app, session
import sqlite3
from ..models import get_db_connection

fixtures_bp = Blueprint('fixtures', __name__, url_prefix='/api')

@fixtures_bp.route('/fixtures', methods=['GET'])
def get_fixtures():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.home_team_id, f.away_team_id, f.date, f.time, f.venue, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        ORDER BY f.date DESC
    """)
    fixtures = cursor.fetchall()
    conn.close()
    fixtures_list = []
    for fixture in fixtures:
        fixtures_list.append({
            'id': fixture[0],
            'home_team': fixture[1],
            'away_team': fixture[2],
            'home_team_id': fixture[3],
            'away_team_id': fixture[4],
            'date': fixture[5],
            'time': fixture[6],
            'venue': fixture[7],
            'home_score': fixture[8],
            'away_score': fixture[9],
            'status': fixture[10]
        })
    return jsonify(fixtures_list)

@fixtures_bp.route('/fixtures/<int:fixture_id>', methods=['GET'])
def get_fixture(fixture_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.date, f.time, f.venue, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        WHERE f.id = ?
    """, (fixture_id,))
    fixture = cursor.fetchone()
    conn.close()
    if fixture:
        return jsonify({
            'id': fixture[0],
            'home_team': fixture[1],
            'away_team': fixture[2],
            'date': fixture[3],
            'time': fixture[4],
            'venue': fixture[5],
            'home_score': fixture[6],
            'away_score': fixture[7],
            'status': fixture[8]
        })
    else:
        return jsonify({'error': 'Fixture not found'}), 404

@fixtures_bp.route('/fixtures', methods=['POST'])
def create_fixture():
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    print(data)
    home_team_name = data.get('home_team_id')
    away_team_name = data.get('away_team_id')
    match_date = data.get('date')
    match_time = data.get('time', '15:00')
    venue = data.get('venue', 'TBD')
    status = data.get('status', 'scheduled')
    home_score = data.get('home_score', 0)
    away_score = data.get('away_score', 0)

    
    if not all([home_team_name, away_team_name, match_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if home_team_name == away_team_name:
        return jsonify({'error': 'Home and away teams cannot be the same'}), 400
    
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    
    # Get team IDs
    cursor.execute("SELECT id FROM teams WHERE id = ?", (home_team_name,))
    home_team_id = cursor.fetchone()
    cursor.execute("SELECT id FROM teams WHERE id = ?", (away_team_name,))
    away_team_id = cursor.fetchone()
    
    if not home_team_id or not away_team_id:
        conn.close()
        return jsonify({'error': 'One or both teams not found'}), 404
    
    try:
        cursor.execute("""
            INSERT INTO fixtures (home_team_id, away_team_id, date, time, venue, status, home_score, away_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (home_team_id[0], away_team_id[0], match_date, match_time, venue, status, home_score, away_score))
        conn.commit()
        fixture_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'message': 'Fixture added successfully', 'id': fixture_id})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@fixtures_bp.route('/fixtures/<int:fixture_id>', methods=['PUT'])
def update_fixture(fixture_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE fixtures 
            SET date = ?, time = ?, venue = ?, status = ?
            WHERE id = ?
        """, (
            data.get('date'),
            data.get('time'),
            data.get('venue'),
            data.get('status'),
            fixture_id
        ))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Fixture not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Fixture updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@fixtures_bp.route('/fixtures/<int:fixture_id>', methods=['DELETE'])
def delete_fixture(fixture_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM fixtures WHERE id = ?", (fixture_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Fixture not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Fixture deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@fixtures_bp.route('/fixtures/<int:fixture_id>/result', methods=['POST'])
def update_result(fixture_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    home_score = data.get('home_score')
    away_score = data.get('away_score')
    
    if home_score is None or away_score is None:
        return jsonify({'error': 'Missing score data'}), 400
    
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE fixtures 
            SET home_score = ?, away_score = ?, status = 'completed'
            WHERE id = ?
        """, (home_score, away_score, fixture_id))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Fixture not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Result updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500 