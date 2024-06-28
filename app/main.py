from app.extensions import app, socketio
from flask_cors import CORS
from app.upload import upload_blueprint

CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(upload_blueprint, url_prefix='/upload')

# Example event handler
@socketio.on("connect")
def handle_connected():
    print("Connected: websocket connected")
    socketio.emit("connect", {"data": "Connected successfully!"})

@socketio.on("file_upload")
def handle_file_upload():
    print("File uploaded: file uploaded successfully")
    socketio.emit("file_upload", {"data": "File uploaded successfully!"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
