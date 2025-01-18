from flask import Blueprint, current_app as app, render_template, session, redirect, url_for
from app.models.leaderboard_models import get_leaderboard_data
from app.database import conn

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
  if 'username' in session:
    socketio = app.socketio
    username = session['username']
    with conn.cursor() as db:
      db.execute(f'''
        SELECT visit_count
        FROM leaderboard
        WHERE username='{username}'
      ''')
      result = db.fetchone()
      previous_score = result[0] if result else 0
      db.execute(f'''
        INSERT INTO leaderboard (username, visit_count)
        VALUES ('{username}', 1)
        ON CONFLICT (username)
        DO UPDATE SET visit_count = leaderboard.visit_count + 1
        RETURNING visit_count
      ''')
      updated_score = db.fetchone()[0]
      conn.commit()

    # Emit leaderboard update only if the score changed
    if updated_score > previous_score:
      leaderboard_data = get_leaderboard_data()
      socketio.emit('update_leaderboard', {'leaderboard': leaderboard_data})

    return render_template('index.html', visit_count=int(updated_score), logged_in=True, username=username)
  else:
    return render_template('index.html', visit_count=0, logged_in=False)

@main_bp.route('/reset')
def reset():
  if 'username' in session:
    username = session['username']
    # reset the visit count for the logged-in user
    with conn.cursor() as db:
      db.execute(f'''
        UPDATE leaderboard SET visit_count=0
        WHERE username='{username}'
      ''')
      conn.commit()
  return redirect(url_for('main.home'))