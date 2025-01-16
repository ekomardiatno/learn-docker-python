from flask import Blueprint, request, session, redirect, url_for, render_template, current_app as app
import redis

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		return redirect(url_for('main.home'))
	return render_template('login.html')

@auth_bp.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('main.home'))

@auth_bp.route('/test_redis')
def test_redis():
	r = app.redis
	try:
		r.ping()
		return "Redis connection is working!"
	except redis.ConnectionError:
		return "Failed to connect to Redis."