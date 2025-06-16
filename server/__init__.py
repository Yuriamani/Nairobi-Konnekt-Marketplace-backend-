from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize instances
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # postgresql://prettyprinted_render_example_d47p_user:ThDsWLD45MGyCvwr5mF8vXerGWMrwF1A@dpg-d10mqls9c44c73dsbffg-a.oregon-postgres.render.com/prettyprinted_render_example_d47p

    # Initialize extensions
    CORS(app, origins='*')
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    # Import and register Blueprints
    from .routes.main import main

    app.register_blueprint(main)

    return app