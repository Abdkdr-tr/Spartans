import sqlite3
import os
from config import DB_PATH

def create_tables():
    # Déduction automatique du dossier parent à partir de DB_PATH
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Création des tables...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            fitness_level TEXT,
            primary_goal TEXT,
            medical_constraints TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            target_body_part TEXT,
            required_equipment TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            target_level TEXT,
            program_goal TEXT,
            required_equipment TEXT,
            embedding_vector BLOB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS program_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER,
            exercise_id INTEGER,
            week_number INTEGER,
            day_number INTEGER,
            set_count INTEGER,
            rep_count TEXT,
            intensity_rate REAL,
            FOREIGN KEY (program_id) REFERENCES workout_programs(id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_active_program (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            program_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (program_id) REFERENCES workout_programs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recommendation_method TEXT,
            user_query TEXT,
            raw_output TEXT,
            execution_time_ms INTEGER,
            user_feedback TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables créées avec succès !")

if __name__ == "__main__":
    create_tables()