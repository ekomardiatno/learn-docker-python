from flask import Flask, render_template, redirect, url_for
import os
import redis

app = Flask(__name__)

# connect to redis
r = redis.Redis(host='redis', port=6379, db=0)

flask_env = os.environ['FLASK_ENV']
debug_mode = True if flask_env == 'development' else False

@app.route('/')
def home():
  visit_count = r.incr('visit_count')
  if visit_count is None:
    visit_count = 0
  else:
    visit_count = int(visit_count)

  return render_template('index.html', visit_count=visit_count)

@app.route('/reset')
def reset():
  r.set('visit_count', 0)
  return redirect(url_for('home'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=debug_mode)