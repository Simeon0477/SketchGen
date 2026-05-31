from flask import Flask
from flask_cors import CORS
from app.routes import router

def create_app():
    app = Flask(__name__, template_folder="templates")
    CORS(app)
    app.register_blueprint(router)
    print("Blueprint enregistré", flush=True)
    return app