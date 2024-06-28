# app/main.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from app.upload import upload_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secret key for session management
CORS(app)  # Enable CORS for all routes

# Initialize SocketIO with CORS support
socketio = SocketIO(app, cors_allowed_origins="*")

# Register blueprints
app.register_blueprint(upload_blueprint, url_prefix='/upload')

# Example event handler
@socketio.on("connect")
def handle_connected():
    print("Connected:", 'webscoket connected')
    emit("connect", {"data": "Connected successfully!"})
    
@socketio.on("file_upload")
def handle_file_upload(data):
    print("file uploaded:", 'file uploaded success fully')
    emit("file_upload", data)
    
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
