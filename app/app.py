from flask import Flask
import os

app = Flask(__name__)

flask_env = os.environ['FLASK_ENV']

@app.route('/')
def home():
  return f"Hello, Docker! {flask_env}"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)