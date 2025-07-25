import sqlite3
import os

def get_db_connection(app):
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app):
    with app.app_context():
        conn = get_db_connection(app)
        cursor = conn.cursor()
        # Create teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                city TEXT,
                coach TEXT,
                logo_url TEXT,
                university TEXT,
                founded TEXT,
                stadium TEXT
            )
        ''')
        # Create players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                team_id INTEGER,
                position TEXT,
                jersey_number INTEGER,
                age INTEGER,
                nationality TEXT,
                height REAL,
                weight REAL,
                photo_url TEXT,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        # Create fixtures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fixtures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                home_team_id INTEGER,
                away_team_id INTEGER,
                home_score INTEGER,
                away_score INTEGER,
                date TEXT,
                time TEXT,
                venue TEXT,
                status TEXT,
                FOREIGN KEY (home_team_id) REFERENCES teams(id),
                FOREIGN KEY (away_team_id) REFERENCES teams(id)
            )
        ''')
        # Create news table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                author TEXT,
                category TEXT,
                image_url TEXT,
                published INTEGER,
                published_at TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close() 