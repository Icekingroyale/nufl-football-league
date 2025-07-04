from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback-secret-key')

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    # Drop existing tables to recreate with new schema
    cursor.execute('DROP TABLE IF EXISTS news')
    cursor.execute('DROP TABLE IF EXISTS fixtures')
    cursor.execute('DROP TABLE IF EXISTS players')
    cursor.execute('DROP TABLE IF EXISTS teams')
    
    # Create Teams table with updated schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            university TEXT,
            city TEXT,
            founded INTEGER,
            coach TEXT,
            stadium TEXT,
            logo_url TEXT
        )
    ''')
    
    # Create Players table with updated schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team_id INTEGER,
            position TEXT,
            jersey_number INTEGER,
            age INTEGER,
            nationality TEXT,
            height INTEGER,
            weight INTEGER,
            photo_url TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    ''')
    
    # Create Fixtures table with updated schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fixtures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            date TEXT,
            time TEXT,
            venue TEXT,
            status TEXT DEFAULT 'scheduled',
            home_score INTEGER,
            away_score INTEGER,
            FOREIGN KEY (home_team_id) REFERENCES teams (id),
            FOREIGN KEY (away_team_id) REFERENCES teams (id)
        )
    ''')
    
    # Create News table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT,
            category TEXT,
            image_url TEXT,
            published BOOLEAN DEFAULT 1,
            created_at TEXT
        )
    ''')
    
    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM teams")
    if cursor.fetchone()[0] == 0:
        # Sample teams
        sample_teams = [
            ('Evangel University Akaeze', 'Evangel University', 'Akaeze', 1994, 'Coach Johnson', 'Evangel Stadium', 'https://via.placeholder.com/150x150?text=EU'),
            ('Ebonyi State University', 'Ebonyi State University', 'Abakaliki', 1980, 'Coach Williams', 'EBSU Stadium', 'https://via.placeholder.com/150x150?text=EBSU'),
            ('University of Nigeria Nsukka', 'University of Nigeria', 'Nsukka', 1960, 'Coach Davis', 'UNN Stadium', 'https://via.placeholder.com/150x150?text=UNN'),
            ('Nnamdi Azikiwe University', 'Nnamdi Azikiwe University', 'Awka', 1970, 'Coach Brown', 'NAU Stadium', 'https://via.placeholder.com/150x150?text=NAU'),
            ('University of Lagos', 'University of Lagos', 'Lagos', 1962, 'Coach Wilson', 'UNILAG Stadium', 'https://via.placeholder.com/150x150?text=UNILAG')
        ]
        cursor.executemany("INSERT INTO teams (name, university, city, founded, coach, stadium, logo_url) VALUES (?, ?, ?, ?, ?, ?, ?)", sample_teams)
        
        # Sample players
        sample_players = [
            ('John Doe', 1, 'Forward', 10, 22, 'Nigerian', 180, 75, 'https://via.placeholder.com/100x100?text=JD'),
            ('Mike Smith', 1, 'Midfielder', 8, 24, 'Nigerian', 175, 70, 'https://via.placeholder.com/100x100?text=MS'),
            ('David Johnson', 2, 'Defender', 4, 23, 'Nigerian', 185, 80, 'https://via.placeholder.com/100x100?text=DJ'),
            ('Chris Wilson', 2, 'Goalkeeper', 1, 25, 'Nigerian', 190, 85, 'https://via.placeholder.com/100x100?text=CW'),
            ('Alex Brown', 3, 'Forward', 9, 21, 'Nigerian', 178, 72, 'https://via.placeholder.com/100x100?text=AB'),
            ('Sam Davis', 3, 'Midfielder', 6, 24, 'Nigerian', 176, 73, 'https://via.placeholder.com/100x100?text=SD'),
            ('Tom Miller', 4, 'Defender', 3, 22, 'Nigerian', 182, 78, 'https://via.placeholder.com/100x100?text=TM'),
            ('Ryan Garcia', 4, 'Forward', 11, 20, 'Nigerian', 177, 71, 'https://via.placeholder.com/100x100?text=RG'),
            ('Kevin Lee', 5, 'Midfielder', 7, 23, 'Nigerian', 174, 69, 'https://via.placeholder.com/100x100?text=KL'),
            ('James Taylor', 5, 'Defender', 5, 25, 'Nigerian', 183, 79, 'https://via.placeholder.com/100x100?text=JT')
        ]
        cursor.executemany("INSERT INTO players (name, team_id, position, jersey_number, age, nationality, height, weight, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_players)
        
        # Sample fixtures
        sample_fixtures = [
            (1, 2, '2024-01-15', '15:00', 'Evangel Stadium', 'completed', 2, 1),
            (3, 4, '2024-01-20', '16:00', 'UNN Stadium', 'completed', 0, 0),
            (5, 1, '2024-01-25', '14:00', 'UNILAG Stadium', 'completed', 1, 3),
            (2, 3, '2024-02-01', '15:30', 'EBSU Stadium', 'scheduled', None, None),
            (4, 5, '2024-02-05', '16:30', 'NAU Stadium', 'scheduled', None, None),
            (1, 3, '2024-02-10', '14:30', 'Evangel Stadium', 'scheduled', None, None)
        ]
        cursor.executemany("INSERT INTO fixtures (home_team_id, away_team_id, date, time, venue, status, home_score, away_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample_fixtures)
        
        # Sample news
        sample_news = [
            ('NUFL Season Kicks Off with Exciting Matches', 'The Nigerian Universities Football League season has officially begun with thrilling opening matches across various campuses. Teams are showing great promise this year.', 'Sports Reporter', 'League News', 'https://via.placeholder.com/400x250?text=NUFL+News', 1, '2024-01-10T10:00:00'),
            ('Evangel University Dominates Opening Match', 'Evangel University Akaeze showed exceptional form in their season opener, securing a convincing 3-1 victory against their rivals.', 'Match Reporter', 'Match Report', 'https://via.placeholder.com/400x250?text=Match+Report', 1, '2024-01-15T18:00:00'),
            ('New Transfer Window Opens for University Teams', 'The transfer window is now open for university teams to strengthen their squads. Several promising players are expected to move between institutions.', 'Transfer News', 'Transfer News', 'https://via.placeholder.com/400x250?text=Transfer+News', 1, '2024-01-12T12:00:00'),
            ('Injury Update: Key Players Return to Training', 'Several key players who were sidelined with injuries have returned to training and are expected to feature in upcoming matches.', 'Medical Team', 'Injury Update', 'https://via.placeholder.com/400x250?text=Injury+Update', 1, '2024-01-14T09:00:00')
        ]
        cursor.executemany("INSERT INTO news (title, content, author, category, image_url, published, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)", sample_news)
    
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
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.date, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        ORDER BY f.date DESC
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
        SELECT t.id, t.name, t.city, t.founded, COUNT(p.id) as player_count
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
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.date, f.home_score, f.away_score, f.status
        FROM fixtures f
        JOIN teams t1 ON f.home_team_id = t1.id
        JOIN teams t2 ON f.away_team_id = t2.id
        ORDER BY f.date DESC
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
                INSERT INTO fixtures (home_team_id, away_team_id, date, status)
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
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.date, f.home_score, f.away_score
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
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/players')
def api_players():
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.name, p.team_id, t.name as team_name, p.position, p.jersey_number, 
               p.age, p.nationality, p.height, p.weight, p.photo_url
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

@app.route('/api/fixtures')
def api_fixtures():
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.id, t1.name as home_team, t2.name as away_team, f.date, f.time, f.venue, 
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
            'away_team': fixture[2],
            'date': fixture[3],
            'time': fixture[4],
            'venue': fixture[5],
            'home_score': fixture[6],
            'away_score': fixture[7],
            'status': fixture[8]
        })
    
    return jsonify(fixtures_list)

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
            INSERT INTO fixtures (home_team_id, away_team_id, date, status)
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

# Teams CRUD API endpoints
@app.route('/api/teams/<int:team_id>', methods=['GET'])
def api_get_team(team_id):
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/teams', methods=['POST'])
def api_create_team():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/teams/<int:team_id>', methods=['PUT'])
def api_update_team(team_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/teams/<int:team_id>', methods=['DELETE'])
def api_delete_team(team_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
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

# Players CRUD API endpoints
@app.route('/api/players/<int:player_id>', methods=['GET'])
def api_get_player(player_id):
    conn = sqlite3.connect('football_league.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    player = cursor.fetchone()
    conn.close()
    
    if player:
        return jsonify({
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
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/api/players', methods=['POST'])
def api_create_player():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/players/<int:player_id>', methods=['PUT'])
def api_update_player(player_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/players/<int:player_id>', methods=['DELETE'])
def api_delete_player(player_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/teams/<int:team_id>/players', methods=['GET'])
def api_get_players_by_team(team_id):
    conn = sqlite3.connect('football_league.db')
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

# Fixtures CRUD API endpoints
@app.route('/api/fixtures/<int:fixture_id>', methods=['GET'])
def api_get_fixture(fixture_id):
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/fixtures', methods=['POST'])
def api_create_fixture():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/fixtures/<int:fixture_id>', methods=['PUT'])
def api_update_fixture(fixture_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/fixtures/<int:fixture_id>', methods=['DELETE'])
def api_delete_fixture(fixture_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/fixtures/<int:fixture_id>/result', methods=['POST'])
def api_update_fixture_result(fixture_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

# News CRUD API endpoints
@app.route('/api/news', methods=['GET'])
def api_get_all_news():
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/news/<int:news_id>', methods=['GET'])
def api_get_news(news_id):
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/news', methods=['POST'])
def api_create_news():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/news/<int:news_id>', methods=['PUT'])
def api_update_news(news_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    conn = sqlite3.connect('football_league.db')
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

@app.route('/api/news/<int:news_id>', methods=['DELETE'])
def api_delete_news(news_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('football_league.db')
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

UPLOAD_FOLDER = '/opt/render/project/src/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename  # You may want to use secure_filename in production
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        url = url_for('uploaded_file', filename=filename, _external=True)
        return jsonify({'url': url}), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('/opt/render/project/src/uploads', filename)

if __name__ == '__main__':
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port) 