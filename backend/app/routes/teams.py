from flask import Blueprint, request, jsonify, current_app, session
import sqlite3
from ..models import get_db_connection

teams_bp = Blueprint('teams', __name__, url_prefix='/api')

@teams_bp.route('/teams', methods=['GET'])
def get_teams():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.name, t.university, t.city, t.founded, t.coach, t.stadium, t.logo_url, COUNT(p.id) as player_count
        FROM teams t
        LEFT JOIN players p ON t.id = p.team_id
        GROUP BY t.id
        ORDER BY t.name
    """)
    teams = cursor.fetchall()
    conn.close()
    teams_list = []
    for team in teams:
        teams_list.append({
            'id': team[0],
            'name': team[1],
            'university': team[2],
            'city': team[3],
            'founded': team[4],
            'coach': team[5],
            'stadium': team[6],
            'logo_url': team[7],
            'player_count': team[8]
        })
    return jsonify(teams_list)

@teams_bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teams WHERE id = ?", (team_id,))
    team = cursor.fetchone()
    conn.close()
    if team:
        return jsonify({
            'id': team[0],
            'name': team[1],
            'university': team[2] if len(team) > 2 else None,
            'city': team[3] if len(team) > 3 else None,
            'founded': team[4] if len(team) > 4 else None,
            'coach': team[5] if len(team) > 5 else None,
            'stadium': team[6] if len(team) > 6 else None,
            'logo_url': team[7] if len(team) > 7 else None
        })
    else:
        return jsonify({'error': 'Team not found'}), 404

@teams_bp.route('/teams', methods=['POST'])
def create_team():
    print('Session contents at team creation:', dict(session))
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO teams (name, university, city, founded, coach, stadium, logo_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('name'),
            data.get('university'),
            data.get('city'),
            data.get('founded'),
            data.get('coach'),
            data.get('stadium'),
            data.get('logo_url')
        ))
        conn.commit()
        team_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Team created successfully', 'id': team_id}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Team name already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/teams/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE teams 
            SET name = ?, university = ?, city = ?, founded = ?, coach = ?, stadium = ?, logo_url = ?
            WHERE id = ?
        """, (
            data.get('name'),
            data.get('university'),
            data.get('city'),
            data.get('founded'),
            data.get('coach'),
            data.get('stadium'),
            data.get('logo_url'),
            team_id
        ))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Team not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Team updated successfully'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Team name already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM teams WHERE id = ?", (team_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Team not found'}), 404
        conn.commit()
        conn.close()
        return jsonify({'message': 'Team deleted successfully'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Cannot delete team with associated players or fixtures'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@teams_bp.route('/teams/<int:team_id>/players', methods=['GET'])
def get_players_by_team(team_id):
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE team_id = ?", (team_id,))
    players = cursor.fetchall()
    conn.close()
    players_list = []
    for player in players:
        players_list.append({
            'id': player[0],
            'name': player[1],
            'team_id': player[2],
            'position': player[3],
            'jersey_number': player[4],
            'age': player[5] if len(player) > 5 else None,
            'nationality': player[6] if len(player) > 6 else None,
            'height': player[7] if len(player) > 7 else None,
            'weight': player[8] if len(player) > 8 else None,
            'photo_url': player[9] if len(player) > 9 else None
        })
    return jsonify(players_list) 