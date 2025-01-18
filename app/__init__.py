from flask import Flask
import os
from flask_session import Session
from flask_socketio import SocketIO
import redis
from .database import close_db_connection, initialize_db
import atexit

def create_app():
  initialize_db()
  atexit.register(close_db_connection)

  app = Flask(__name__)
  app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

  app.redis = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), decode_responses=True)

  # Setup Flask-Session to use Redis as a backend
  app.config['SESSION_TYPE'] = 'redis'
  app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis', port=6379)
  app.config['SESSION_PERMANENT'] = False
  app.config['SESSION_USE_SIGNER'] = True
  Session(app)

  # initialize socketio
  socketio = SocketIO(app)
  from .socketio.events import register_socketio_events
  register_socketio_events(socketio)

  app.socketio = socketio

  # import and register blueprint
  from .routes.auth_routes import auth_bp
  from .routes.main_routes import main_bp
  from .routes.leaderboard_routes import leaderboard_bp
  app.register_blueprint(auth_bp)
  app.register_blueprint(main_bp)
  app.register_blueprint(leaderboard_bp)

  return app