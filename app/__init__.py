from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
app_jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    app_jwt.init_app(app, True)

    from app.jwt.helper import (user_lookup_callback,
                                make_additional_claims,
                                missing_token_callback,
                                invalid_token_callback,
                                expired_token_callback)
    app_jwt.user_lookup_loader(user_lookup_callback)
    app_jwt.additional_claims_loader(make_additional_claims)
    app_jwt.expired_token_loader(expired_token_callback)
    app_jwt.invalid_token_loader(invalid_token_callback)
    app_jwt.unauthorized_loader(missing_token_callback)

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.login_route import login_bp
    from app.routes.product_routes import product_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(product_bp, url_prefix='/product')

    return app
