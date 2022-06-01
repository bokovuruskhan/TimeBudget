from flask import Flask
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy


class MyApp:
    app = Flask(__name__)
    app.debug = True
    app.config["SECRET_KEY"] = "\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    babel = Babel(app)
    database = SQLAlchemy(app)
    ENCODING = "UTF-8"
