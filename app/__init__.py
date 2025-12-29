from flask import Flask

from .routes import home_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
