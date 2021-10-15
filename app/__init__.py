from flask import Flask
import datetime
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = Flask(__name__)

app.secret_key = "SHHHHH"
app.config["JWT_SECRET_KEY"] = "dev_on_deck"  # Change this!
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    minutes=240)  # Change this!
# app.config['JWT_REFRESH_EXPIRATION_DELTA'] = datetime.timedelta(days=30)
# app.config["JWT_EXPIRATION_DELTA"] = False
# app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(days=100)
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)
jwt = JWTManager(app)
CORS(app)
