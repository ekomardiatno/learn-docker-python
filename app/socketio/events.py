from flask import request
from flask_socketio import emit

def register_socketio_events(socketio):
  connected_users = {}

  @socketio.on('connect')
  def handle_connect():
    connected_users[request.sid] = {'username': None}
    print(f"New connection: {request.sid}")

  @socketio.on('set_username')
  def set_username(data):
    connected_users[request.sid]['username'] = data['username']

  @socketio.on('disconnect')
  def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
    connected_users.pop(request.sid, None)

  @socketio.on_error('connect')
  def handle_connect_error(error):
    print(f"Error during connection: {error}")
    # Handle error or send a message to the client
    emit('error', {'message': 'Connection error occurred! Please try again later.'})