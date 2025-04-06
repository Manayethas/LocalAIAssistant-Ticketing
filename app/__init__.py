from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ Set a secure secret key for sessions
    app.config['SECRET_KEY'] = 'this-should-be-random-and-secret'

    # ✅ Database config (adjust if needed)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/tickets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.main import main
    app.register_blueprint(main)

    return app
