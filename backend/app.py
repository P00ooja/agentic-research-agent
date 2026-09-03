from flask import Flask
from flask_cors import CORS
from config import config
import os

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # CORS support
    CORS(app)
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'healthy'}, 200
    
    # Register API blueprint
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=app.config['SERVER_PORT'],
        debug=app.config['FLASK_DEBUG']
    )
