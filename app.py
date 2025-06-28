from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    # Create Teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            city TEXT,
            founded_year INTEGER
        )
    ''')
    
    # Create Players table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team_id INTEGER,
            position TEXT,
            jersey_number INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    ''')
    
    # Create Fixtures table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            match_date TEXT,
            home_score INTEGER,
            away_score INTEGER,
            status TEXT DEFAULT 'scheduled',
            FOREIGN KEY (home_team_id) REFERENCES teams (id),
            FOREIGN KEY (away_team_id) REFERENCES teams (id)
        )
    ''')
    
    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM teams")
    if cursor.fetchone()[0] == 0:
        # Sample teams
        sample_teams = [
            ('Evangel University Akaeze', 'Akaeze', 1994),
            ('Ebonyi State University', 'Abakaliki', 1980),
            ('University of Nigeria Nsukka', 'Nsukka', 1960),
            ('Nnamdi Azikiwe University', 'Awka', 1970),
            ('University of Lagos', 'Lagos', 1962)
        ]
        cursor.executemany("INSERT INTO teams (name, city, founded_year) VALUES (?, ?, ?)", sample_teams)
        
        # Sample players
        sample_players = [
            ('John Doe', 1, 'Forward', 10),
            ('Mike Smith', 1, 'Midfielder', 8),
            ('David Johnson', 2, 'Defender', 4),
            ('Chris Wilson', 2, 'Goalkeeper', 1),
            ('Alex Brown', 3, 'Forward', 9),
            ('Sam Davis', 3, 'Midfielder', 6),
            ('Tom Miller', 4, 'Defender', 3),
            ('Ryan Garcia', 4, 'Forward', 11),
            ('Kevin Lee', 5, 'Midfielder', 7),
            ('James Taylor', 5, 'Defender', 5)
        ]
        cursor.executemany("INSERT INTO players (name, team_id, position, jersey_number) VALUES (?, ?, ?, ?)", sample_players)
        
        # Sample fixtures
        sample_fixtures = [
            (1, 2, '2024-01-15', 2, 1, 'completed'),
            (3, 4, '2024-01-20', 0, 0, 'completed'),
            (5, 1, '2024-01-25', 1, 3, 'completed'),
            (2, 3, '2024-02-01', None, None, 'scheduled'),
            (4, 5, '2024-02-05', None, None, 'scheduled'),
            (1, 3, '2024-02-10', None, None, 'scheduled')
        ]
        cursor.executemany("INSERT INTO fixtures (home_team_id, away_team_id, match_date, home_score, away_score, status) VALUES (?, ?, ?, ?, ?, ?)", sample_fixtures)
    
    conn.commit()
    conn.close()

# Helper function to get league table
def get_league_table():
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM teams")
    teams = cursor.fetchall()
    
    league_table = []
    
    for team_id, team_name in teams:
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
            'team_name': team_name,
            'matches_played': matches_played,
            'points': points,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goal_difference
        })
    
    league_table.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)
    
    conn.close()
    return league_table

# Routes
@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.match_date, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        ORDER BY f.match_date DESC
        LIMIT 5
    """)
    recent_fixtures = cursor.fetchall()
    
    league_table = get_league_table()
    
    conn.close()
    
    return render_template('index.html', recent_fixtures=recent_fixtures, league_table=league_table)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/teams')
def teams():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.id, t.name, t.city, t.founded_year, COUNT(p.id) as player_count
        FROM teams t
        LEFT JOIN players p ON t.id = p.team_id
        GROUP BY t.id
        ORDER BY t.name
    """)
    teams = cursor.fetchall()
    
    conn.close()
    
    return render_template('teams.html', teams=teams)

@app.route('/players')
def players():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.name, t.name as team_name, p.position, p.jersey_number
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        ORDER BY t.name, p.name
    """)
    players = cursor.fetchall()
    
    conn.close()
    
    return render_template('players.html', players=players)

@app.route('/fixtures')
def fixtures():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.match_date, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        ORDER BY f.match_date DESC
    """)
    fixtures = cursor.fetchall()
    
    conn.close()
    
    return render_template('fixtures.html', fixtures=fixtures)

@app.route('/add_fixture', methods=['GET', 'POST'])
def add_fixture():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        match_date = request.form['match_date']
        
        if home_team_id == away_team_id:
            flash('Home and away teams cannot be the same!', 'error')
        else:
            conn = sqlite3.connect('football_league.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO fixtures (home_team_id, away_team_id, match_date, status)
                VALUES (?, ?, ?, 'scheduled')
            """, (home_team_id, away_team_id, match_date))
            
            conn.commit()
            conn.close()
            
            flash('Fixture added successfully!', 'success')
            return redirect(url_for('fixtures'))
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM teams ORDER BY name")
    teams = cursor.fetchall()
    conn.close()
    
    return render_template('add_fixture.html', teams=teams)

@app.route('/update_result/<int:fixture_id>', methods=['GET', 'POST'])
def update_result(fixture_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        home_score = request.form['home_score']
        away_score = request.form['away_score']
        
        conn = sqlite3.connect('football_league.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE fixtures 
            SET home_score = ?, away_score = ?, status = 'completed'
            WHERE id = ?
        """, (home_score, away_score, fixture_id))
        
        conn.commit()
        conn.close()
        
        flash('Result updated successfully!', 'success')
        return redirect(url_for('fixtures'))
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.match_date, f.home_score, f.away_score
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        WHERE f.id = ?
    """, (fixture_id,))
    
    fixture = cursor.fetchone()
    conn.close()
    
    if not fixture:
        flash('Fixture not found!', 'error')
        return redirect(url_for('fixtures'))
    
    return render_template('update_result.html', fixture=fixture)

@app.route('/api/league_table')
def api_league_table():
    league_table = get_league_table()
    return jsonify(league_table)

# API Endpoints for React Frontend
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'admin123':
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'success': True, 'message': 'Login successful', 'user': {'username': username}})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logout successful'})

@app.route('/api/check_auth')
def api_check_auth():
    if 'logged_in' in session:
        return jsonify({'authenticated': True, 'user': {'username': session.get('username')}})
    else:
        return jsonify({'authenticated': False}), 401

@app.route('/api/teams')
def api_teams():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.id, t.name, t.city, t.founded_year, COUNT(p.id) as player_count
        FROM teams t
        LEFT JOIN players p ON t.id = p.team_id
        GROUP BY t.id
        ORDER BY t.name
    """)
    teams_data = cursor.fetchall()
    
    teams = []
    for team in teams_data:
        teams.append({
            'id': team[0],
            'name': team[1],
            'city': team[2],
            'founded_year': team[3],
            'player_count': team[4]
        })
    
    conn.close()
    return jsonify(teams)

@app.route('/api/players')
def api_players():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.name, t.name as team_name, p.position, p.jersey_number
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.id
        ORDER BY t.name, p.name
    """)
    players_data = cursor.fetchall()
    
    players = []
    for player in players_data:
        players.append({
            'id': player[0],
            'name': player[1],
            'team_name': player[2],
            'position': player[3],
            'jersey_number': player[4]
        })
    
    conn.close()
    return jsonify(players)

@app.route('/api/fixtures')
def api_fixtures():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.match_date, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        ORDER BY f.match_date DESC
    """)
    fixtures_data = cursor.fetchall()
    
    fixtures = []
    for fixture in fixtures_data:
        fixtures.append({
            'id': fixture[0],
            'home_team': fixture[1],
            'away_team': fixture[2],
            'match_date': fixture[3],
            'home_score': fixture[4],
            'away_score': fixture[5],
            'status': fixture[6]
        })
    
    conn.close()
    return jsonify(fixtures)

@app.route('/api/add_fixture', methods=['POST'])
def api_add_fixture():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    home_team_name = data.get('home_team')
    away_team_name = data.get('away_team')
    match_date = data.get('match_date')
    
    if not all([home_team_name, away_team_name, match_date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if home_team_name == away_team_name:
        return jsonify({'error': 'Home and away teams cannot be the same'}), 400
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    # Get team IDs
    cursor.execute("SELECT id FROM teams WHERE name = ?", (home_team_name,))
    home_team_id = cursor.fetchone()
    
    cursor.execute("SELECT id FROM teams WHERE name = ?", (away_team_name,))
    away_team_id = cursor.fetchone()
    
    if not home_team_id or not away_team_id:
        conn.close()
        return jsonify({'error': 'One or both teams not found'}), 404
    
    try:
        cursor.execute("""
            INSERT INTO fixtures (home_team_id, away_team_id, match_date, status)
            VALUES (?, ?, ?, 'scheduled')
        """, (home_team_id[0], away_team_id[0], match_date))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Fixture added successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_result/<int:fixture_id>', methods=['POST'])
def api_update_result(fixture_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    home_score = data.get('home_score')
    away_score = data.get('away_score')
    
    if home_score is None or away_score is None:
        return jsonify({'error': 'Missing score data'}), 400
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/stats')
def api_stats():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    # Get total teams
    cursor.execute("SELECT COUNT(*) FROM teams")
    total_teams = cursor.fetchone()[0]
    
    # Get total players
    cursor.execute("SELECT COUNT(*) FROM players")
    total_players = cursor.fetchone()[0]
    
    # Get total fixtures
    cursor.execute("SELECT COUNT(*) FROM fixtures")
    total_fixtures = cursor.fetchone()[0]
    
    # Get completed matches
    cursor.execute("SELECT COUNT(*) FROM fixtures WHERE status = 'completed'")
    completed_matches = cursor.fetchone()[0]
    
    # Get upcoming matches
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 