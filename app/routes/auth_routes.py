from flask import Blueprint, request, session, redirect, url_for, render_template, current_app as app
import redis
from flask_dance.contrib.google import make_google_blueprint, google
import os

auth_bp = Blueprint('auth', __name__)
google_bp = make_google_blueprint(
	client_id=os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID'),
	client_secret=os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET'),
	scope=[
		"https://www.googleapis.com/auth/userinfo.email",
		"https://www.googleapis.com/auth/userinfo.profile",
		"openid"
	],
	redirect_to="auth.login_google"
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_web():
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		return redirect(url_for('main.home'))
	return render_template('login.html')

@auth_bp.route('/login/google')
def login_google():
	if not google.authorized:
		return redirect(url_for("google.login"))
	resp = google.get("/oauth2/v1/userinfo")
	user_info = resp.json()
	username = user_info["email"]
	session['username'] = username
	return redirect(url_for('main.home'))

@auth_bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("main.home"))

@auth_bp.route('/test_redis')
def test_redis():
	r = app.redis
	try:
		r.ping()
		return "Redis connection is working!"
	except redis.ConnectionError:
		return "Failed to connect to Redis."