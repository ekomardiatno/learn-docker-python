from flask import current_app as app
from app.database import conn

def get_leaderboard_data():
  with conn.cursor() as db:
    db.execute('''
      SELECT username, visit_count
      FROM leaderboard
      ORDER BY visit_count DESC
    ''')
    results = db.fetchall()
    return [{'username': row[0], 'visit_count': row[1]} for row in results]