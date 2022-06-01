from flask import render_template

import admin
from config import MyApp

app = MyApp.app
database = MyApp.database
babel = MyApp.babel


@babel.localeselector
def get_locale():
    return "ru"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    database.create_all()
    admin.config()
    app.run()
