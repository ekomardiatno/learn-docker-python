from flask import Blueprint, session, current_app as app, redirect, url_for, render_template, request

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/leaderboard')
def leaderboard():
  redis = app.redis
  # Get the current page number from the query string (default is 1)
  page = int(request.args.get('page', 1))
  per_page = 5
  
  # calculate start and end indices for redis
  start = (page - 1) * per_page
  end = start + per_page - 1
  
	# Get the top 5 users from the leaderboard
  top_users = redis.zrevrange('leaderboard', start, end, withscores=True)
  
	# convert the redis data into a list of dictionaries
  leaderboard = [{ 'username': user, 'visit_count': int(score) } for user, score in top_users]
  
	# get the total number of users in the leaderboard
  total_users = redis.zcard('leaderboard')
  total_pages = (total_users + per_page - 1) // per_page # calculate total pages
  
  return render_template(
    'leaderboard.html',
    leaderboard=leaderboard,
    current_page=page,
    total_pages=total_pages
  )