from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your actual secret key

socketio = SocketIO(app, cors_allowed_origins="*")
