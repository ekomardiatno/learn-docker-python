from flask import Blueprint, session, current_app as app, redirect, url_for, render_template, request
from app.database import conn

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/leaderboard')
def leaderboard():
  # Get the current page number from the query string (default is 1)
  page = int(request.args.get('page', 1))
  per_page = 5
  
  # calculate offset
  offset = (page - 1) * per_page
  
	# Get the top 5 users from the leaderboard
  with conn.cursor() as cur:
    cur.execute(f'''
      SELECT username, visit_count FROM leaderboard
      ORDER BY visit_count DESC
      LIMIT {per_page} OFFSET {offset}
    ''')
    top_users = cur.fetchall()
  
	# convert the data into a list of dictionaries
  leaderboard = [{'username': row[0], 'visit_count': row[1]} for row in top_users]
  
	# get the total number of users in the leaderboard
  with conn.cursor() as cur:
    cur.execute('''
      SELECT COUNT(*) FROM leaderboard
    ''')
    total_users = cur.fetchone()[0]

  total_pages = (total_users + per_page - 1) // per_page # calculate total pages
  
  return render_template(
    'leaderboard.html',
    leaderboard=leaderboard,
    current_page=page,
    total_pages=total_pages
  )