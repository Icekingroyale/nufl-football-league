from flask import Blueprint, request, jsonify, current_app, session
import sqlite3
from ..models import get_db_connection

fixtures_bp = Blueprint('fixtures', __name__, url_prefix='/api/fixtures')

@fixtures_bp.route('', methods=['GET'])
def get_fixtures():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t1.logo_url as home_logo, t2.name as away_team, t2.logo_url as away_logo, f.date, f.time, f.venue, \
               f.home_score, f.away_score, f.status
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
            'home_logo': fixture[2],
            'away_team': fixture[3],
            'away_logo': fixture[4],
            'date': fixture[5],
            'time': fixture[6],
            'venue': fixture[7],
            'home_score': fixture[8],
            'away_score': fixture[9],
            'status': fixture[10]
        })
    return jsonify(fixtures_list)

@fixtures_bp.route('/<int:fixture_id>', methods=['GET'])
def get_fixture(fixture_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fixtures WHERE id = ?", (fixture_id,))
    fixture = cursor.fetchone()
    conn.close()
    if fixture:
        return jsonify({
            'id': fixture[0],
            'home_team_id': fixture[1],
            'away_team_id': fixture[2],
            'date': fixture[3],
            'time': fixture[4] if len(fixture) > 4 else None,
            'venue': fixture[5] if len(fixture) > 5 else None,
            'status': fixture[6] if len(fixture) > 6 else 'scheduled',
            'home_score': fixture[7] if len(fixture) > 7 else None,
            'away_score': fixture[8] if len(fixture) > 8 else None
        })
    else:
        return jsonify({'error': 'Fixture not found'}), 404

@fixtures_bp.route('', methods=['POST'])
def create_fixture():
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO fixtures (home_team_id, away_team_id, date, time, venue, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get('home_team_id'),
            data.get('away_team_id'),
            data.get('date'),
            data.get('time'),
            data.get('venue'),
            data.get('status', 'scheduled')
        ))
        conn.commit()
        fixture_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Fixture created successfully', 'id': fixture_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@fixtures_bp.route('/<int:fixture_id>', methods=['PUT'])
def update_fixture(fixture_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE fixtures 
            SET home_team_id = ?, away_team_id = ?, date = ?, time = ?, venue = ?, status = ?
            WHERE id = ?
        """, (
            data.get('home_team_id'),
            data.get('away_team_id'),
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

@fixtures_bp.route('/<int:fixture_id>', methods=['DELETE'])
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

@fixtures_bp.route('/<int:fixture_id>/result', methods=['POST'])
def update_fixture_result(fixture_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE fixtures 
            SET home_score = ?, away_score = ?, status = ?
            WHERE id = ?
        """, (
            data.get('home_score'),
            data.get('away_score'),
            'completed',
            fixture_id
        ))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Fixture not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Fixture result updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500 