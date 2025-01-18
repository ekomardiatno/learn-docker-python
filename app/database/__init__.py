import psycopg
import os

# Connect to PostgreSQL
conn = psycopg.connect(
  host=os.getenv('POSTGRES_HOST', 'db'),
  dbname=os.getenv('POSTGRES_DB', 'leaderboard'),
  user=os.getenv('POSTGRES_USER', 'postgres'),
  password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
)

def close_db_connection():
  if conn:
    conn.close()

def initialize_db():
  with conn.cursor() as db:
    db.execute('''
      CREATE TABLE IF NOT EXISTS leaderboard (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        visit_count INT DEFAULT 0
      );
    ''')
    conn.commit()