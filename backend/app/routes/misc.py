from flask import Blueprint, jsonify, redirect, current_app, session
import sqlite3
from ..models import get_db_connection

misc_bp = Blueprint('misc', __name__)

@misc_bp.route('/')
def index():
    return jsonify({
        'message': 'NUFL Football League API',
        'status': 'running',
        'endpoints': {
            'players': '/api/players',
            'teams': '/api/teams',
            'fixtures': '/api/fixtures',
            'news': '/api/news',
            'league_table': '/api/league_table'
        }
    })

@misc_bp.route('/teams')
def teams_redirect():
    return redirect('/api/teams')

@misc_bp.route('/players')
def players_redirect():
    return redirect('/api/players')

@misc_bp.route('/fixtures')
def fixtures_redirect():
    return redirect('/api/fixtures')

@misc_bp.route('/api/league_table')
def api_league_table():
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, logo_url FROM teams")
    teams = cursor.fetchall()
    league_table = []
    for team_id, team_name, logo_url in teams:
        cursor.execute("""
            SELECT 
                SUM(CASE 
                    WHEN home_team_id = ? AND home_score > away_score THEN 3
                    WHEN away_team_id = ? AND away_score > home_score THEN 3
                    WHEN (home_team_id = ? OR away_team_id = ?) AND home_score = away_score THEN 1
                    ELSE 0
                END) as points,
                SUM(CASE 
                    WHEN home_team_id = ? THEN home_score
                    WHEN away_team_id = ? THEN away_score
                    ELSE 0
                END) as goals_for,
                SUM(CASE 
                    WHEN home_team_id = ? THEN away_score
                    WHEN away_team_id = ? THEN home_score
                    ELSE 0
                END) as goals_against,
                COUNT(CASE 
                    WHEN (home_team_id = ? OR away_team_id = ?) AND status = 'completed' THEN 1
                END) as matches_played
            FROM fixtures 
            WHERE status = 'completed' AND (home_team_id = ? OR away_team_id = ?)
        """, (team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id))
        result = cursor.fetchone()
        points = result[0] or 0
        goals_for = result[1] or 0
        goals_against = result[2] or 0
        matches_played = result[3] or 0
        goal_difference = goals_for - goals_against
        league_table.append({
            'team_id': team_id,
            'team_name': team_name,
            'logo_url': logo_url,
            'matches_played': matches_played,
            'points': points,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goal_difference
        })
    league_table.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)
    conn.close()
    return jsonify(league_table)

@misc_bp.route('/api/stats')
def api_stats():
    if 'auth_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM teams")
    total_teams = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM players")
    total_players = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fixtures")
    total_fixtures = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fixtures WHERE status = 'completed'")
    completed_matches = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fixtures WHERE status = 'scheduled'")
    upcoming_matches = cursor.fetchone()[0]
    conn.close()
    stats = {
        'total_teams': total_teams,
        'total_players': total_players,
        'total_fixtures': total_fixtures,
        'completed_matches': completed_matches,
        'upcoming_matches': upcoming_matches
    }
    return jsonify(stats) 