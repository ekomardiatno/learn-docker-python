from app import create_app
import os

app = create_app()
socketio = app.socketio
port = int(os.getenv('PORT', 5000))
flask_env = os.getenv('FLASK_ENV')

if __name__ == '__main__':
  import eventlet
  socketio.run(app, host='0.0.0.0', port=port, debug=True if flask_env == 'development' else False)