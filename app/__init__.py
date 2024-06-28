from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration for file uploads
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    from .upload import upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')

    return app
