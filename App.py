from flask import Flask
from routes.productos import productos
from routes.usuarios import usuarios
from routes.auth import auth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Mysql connection
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLAlchemy(app)
# Settings
app.secret_key = "mysecretkey"

# Blueprints imports
app.register_blueprint(productos)
app.register_blueprint(usuarios)
app.register_blueprint(auth)


