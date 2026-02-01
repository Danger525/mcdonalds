

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

import logging


print("Importing app package...")


from config import config
from .extensions import db, migrate, jwt, cache, limiter


def create_app(config_name='default'):


    print("Init App Factory")
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Enable CORS for API
    app.config.from_object(config[config_name])


    # Initialize Extensions
    print("Init DB")
    db.init_app(app)
    print("Init Migrate")
    migrate.init_app(app, db)
    print("Init JWT")
    jwt.init_app(app)
    print("Init Cache")
    cache.init_app(app)
    print("Init Limiter")
    limiter.init_app(app)
    
    from .extensions import socketio

    # socketio.init_app(app, cors_allowed_origins="*")
 # Allow all for dev
    

    # Import Events
    # from . import events

    
    # Rate Limit Configuration
    limiter.default_limits = ["200 per day", "50 per hour"]


    # Logging
    import logging
    from logging.handlers import RotatingFileHandler
    # if not app.debug: (Enable logging always for now)
    file_handler = RotatingFileHandler('menu_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Menu App Startup')

    # Register Blueprints
    # Register Blueprints
    from .api import auth_bp, menu_bp, orders_bp, admin_bp, cart_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')

    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/admin')
    def admin_ui():
        return render_template('admin.html')
        
    @app.route('/admin/qr-print')
    def qr_print():
        return render_template('qr_admin.html')

    @app.route('/status/<int:id>')
    def order_status_ui(id):
        return render_template('status.html')

    return app
