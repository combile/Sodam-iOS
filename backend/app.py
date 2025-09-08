from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt, jwt, cors
from .blueprints.api import api_bp
from .blueprints.auth import auth_bp
from .blueprints.recs import recs_bp

def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Blueprints (namespaced under /api/v1)
    app.register_blueprint(api_bp,  url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(recs_bp, url_prefix="/api/v1/recs")
    return app
