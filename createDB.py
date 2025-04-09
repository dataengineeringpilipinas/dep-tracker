# build_location_db.py
import sqlite3
from datetime import datetime
from contextlib import closing

DATABASE_NAME = 'location_tracker.db'

def create_database():
    """Create the SQLite database with locations table"""
    try:
        with closing(sqlite3.connect(DATABASE_NAME)) as conn:
            with conn:
                # Create locations table
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
                
                # Create index on username for faster lookups
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_username 
                    ON locations (username)
                """)
                
                print(f"Successfully created database '{DATABASE_NAME}' with locations table")
                
                # Verify table structure
                cursor = conn.execute("PRAGMA table_info(locations)")
                columns = cursor.fetchall()
                print("\nTable structure:")
                print("| {:<3} | {:<20} | {:<8} | {:<5} |".format("cid", "name", "type", "notnull"))
                print("-" * 50)
                for col in columns:
                    print("| {:<3} | {:<20} | {:<8} | {:<5} |".format(
                        col[0], col[1], col[2], col[3]))
                
                return True
                
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == '__main__':
    print("Building location tracking database...")
    if create_database():
        print("\nDatabase setup completed successfully!")
    else:
        print("\nDatabase setup failed.")