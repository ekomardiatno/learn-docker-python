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
		visit_count = r.incr(f'{username}_visit_count')
		if visit_count is None:
				visit_count = 0
		else:
				visit_count = int(visit_count)

		return render_template('index.html', visit_count=visit_count, logged_in=True, username=username)
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
  r.set('visit_count', 0)
  return redirect(url_for('home'))

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