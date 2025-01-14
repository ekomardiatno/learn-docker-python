from flask import Flask
import os
import redis

app = Flask(__name__)

# connect to redis
r = redis.Redis(host='redis', port=6379, db=0)

flask_env = os.environ['FLASK_ENV']
debug_mode = True if flask_env == 'development' else False

@app.route('/')
def home():
  return "Hello, Docker!"

@app.route('/flask-env')
def flask_env():
  return f"Flask ENV: {flask_env}"

@app.route('/visit-count')
def visit_count():
  visit_count = r.incr('visit_count')
  return f"This page has been visited {visit_count}"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=debug_mode)