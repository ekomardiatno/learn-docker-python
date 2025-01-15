from flask import Flask, render_template, redirect, url_for, request, session
import redis
from flask_session import Session

app = Flask(__name__)

# connect to redis
r = redis.Redis(host='redis', port=6379, db=0)
# Secret key for session management
app.secret_key = 'supersecretkey'

# Setup Flask-Session to use Redis as a backend
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis', port=6379)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

@app.route('/')
def home():
	if 'username' in session:
		# Get and increase the current user's visit count from Redis
		username = session['username']
		# increment the visit count for the logged0in user
		r.zincrby('leaderboard', 1, username)
		visit_count = r.zscore('leaderboard', username)
		return render_template('index.html', visit_count=int(visit_count), logged_in=True, username=username)
	else:
		return render_template('index.html', visit_count=0, logged_in=False)

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
	# Get the top 5 users from the leaderboard
	top_users = r.zrevrange('leaderboard', 0, 4, withscores=True)
	leaderboard = [{ 'username': user.decode('utf-8'), 'visit_count': int(score) } for user, score in top_users]
	return render_template('leaderboard.html', leaderboard=leaderboard)

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
  app.run(host='0.0.0.0', port=5000)