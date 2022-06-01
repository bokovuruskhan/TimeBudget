from flask import render_template, request
from model import Week, Todo
import admin
from config import MyApp

app = MyApp.app
database = MyApp.database
babel = MyApp.babel


@babel.localeselector
def get_locale():
    return "ru"


@app.route("/todo/add", methods=["POST"])
def add_todo():
    day_id = request.form.get("day_id")
    name = request.form.get("name")
    Todo.add(name, day_id)
    return index()


@app.route("/")
def index():
    Week.init_week()
    return render_template("index.html", week=Week.get_current_week())


if __name__ == '__main__':
    database.create_all()
    admin.config()
    app.run()
