from flask import Blueprint, current_app as app, render_template, session, redirect, url_for
from app.models.leaderboard_models import get_leaderboard_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
  if 'username' in session:
    redis = app.redis
    socketio = app.socketio
    username = session['username']
    previous_score = redis.zscore('leaderboard', username) or 0
    updated_score = redis.zincrby('leaderboard', 1, username)

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
    redis = app.redis
    username = session['username']
    # reset the visit count for the logged-in user
    redis.zadd('leaderboard', { username: 0 })
  return redirect(url_for('main.home'))