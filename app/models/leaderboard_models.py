from flask import current_app as app

def get_leaderboard_data():
  redis = app.redis
  top_users = redis.zrevrange('leaderboard', 0, 9, withscores=True)
  return [{'username': user, 'visit_count': int(score)} for user, score in top_users]