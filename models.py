import sqlite3
from datetime import datetime
from contextlib import closing

DATABASE = 'location_tracker.db'

def init_db():
    """Initialize the database"""
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    submission_timestamp TEXT NOT NULL,
                    last_update_timestamp TEXT NOT NULL
                )
            """)

def save_location(username, latitude, longitude):
    """Save or update a location in the database"""
    current_time = datetime.utcnow().isoformat()
    
    with closing(sqlite3.connect(DATABASE)) as conn:
        with conn:
            cursor = conn.execute(
                "SELECT id FROM locations WHERE username = ?", 
                (username,)
            )
            if cursor.fetchone():
                conn.execute(
                    """UPDATE locations 
                    SET latitude = ?, longitude = ?, last_update_timestamp = ?
                    WHERE username = ?""",
                    (latitude, longitude, current_time, username)
                )
                action = "updated"
            else:
                conn.execute(
                    """INSERT INTO locations 
                    (username, latitude, longitude, submission_timestamp, last_update_timestamp)
                    VALUES (?, ?, ?, ?, ?)""",
                    (username, latitude, longitude, current_time, current_time)
                )
                action = "created"
    return action

def get_all_locations():
    """Retrieve all locations from the database"""
    with closing(sqlite3.connect(DATABASE)) as conn:
        cursor = conn.execute(
            "SELECT username, latitude, longitude, submission_timestamp, last_update_timestamp FROM locations"
        )
        return [
            {
                "username": row[0],
                "latitude": row[1],
                "longitude": row[2],
                "submission_timestamp": row[3],
                "last_update_timestamp": row[4]
            }
            for row in cursor.fetchall()
        ]