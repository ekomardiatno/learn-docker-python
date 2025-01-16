from flask import Flask, render_template, redirect, url_for, request, session
import redis
from flask_session import Session
import os
from flask_socketio import SocketIO, emit

flask_env = os.getenv('FLASK_ENV')

app = Flask(__name__)
# Secret key for session management
app.secret_key = os.urandom(24)

# connect to redis
r = redis.Redis(host='redis', port=6379, db=0)

# Setup Flask-Session to use Redis as a backend
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis', port=6379)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

socketio = SocketIO(app)
connected_users = {}

@socketio.on('connect')
def handle_connect():
	connected_users[request.sid] = {'username': None}
	print(f"New connection: {request.sid}")

@socketio.on('set_username')
def set_username(data):
	connected_users[request.sid]['username'] = data['username']

@socketio.on('disconnect')
def handle_disconnect():
	print(f"Client disconnected: {request.sid}")
	connected_users.pop(request.sid, None)

@app.route('/')
def home():
	if 'username' in session:
		username = session['username']
		previous_score = r.zscore('leaderboard', username) or 0
		updated_score = r.zincrby('leaderboard', 1, username)

		# Emit leaderboard update only if the score changed
		if updated_score > previous_score:
			leaderboard_data = get_leaderboard_data()
			socketio.emit('update_leaderboard', {'leaderboard': leaderboard_data})

		return render_template('index.html', visit_count=int(updated_score), logged_in=True, username=username)
	else:
		return render_template('index.html', visit_count=0, logged_in=False)

def get_leaderboard_data():
	top_users = r.zrevrange('leaderboard', 0, 9, withscores=True)
	return [{'username': user.decode('utf-8'), 'visit_count': int(score)} for user, score in top_users]

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		return redirect(url_for('home'))
	return render_template('login.html')

@app.route('/reset')
def reset():
  if 'username' in session:
    username = session['username']
    # reset the visit count for the logged-in user
    r.zadd('leaderboard', { username: 0 })
  return redirect(url_for('home'))

@app.route('/leaderboard')
def leaderboard():
  # Get the current page number from the query string (default is 1)
  page = int(request.args.get('page', 1))
  per_page = 5
  
  # calculate start and end indices for redis
  start = (page - 1) * per_page
  end = start + per_page - 1
  
	# Get the top 5 users from the leaderboard
  top_users = r.zrevrange('leaderboard', start, end, withscores=True)
  
	# convert the redis data into a list of dictionaries
  leaderboard = [{ 'username': user.decode('utf-8'), 'visit_count': int(score) } for user, score in top_users]
  
	# get the total number of users in the leaderboard
  total_users = r.zcard('leaderboard')
  total_pages = (total_users + per_page - 1) // per_page # calculate total pages
  
  return render_template(
    'leaderboard.html',
    leaderboard=leaderboard,
    current_page=page,
    total_pages=total_pages
  )

@app.route('/test_redis')
def test_redis():
	try:
		r.ping()
		return "Redis connection is working!"
	except redis.ConnectionError:
		return "Failed to connect to Redis."

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('home'))

if __name__ == '__main__':
	import eventlet
	socketio.run(app, host='0.0.0.0', port=5000, debug=True if flask_env == 'development' else False)