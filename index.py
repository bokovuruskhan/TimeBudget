from datetime import datetime
from flask_login import login_required, LoginManager, logout_user, login_user, current_user
from flask import render_template, request, send_from_directory
from model import Week, Todo, save, find_by_id, delete, get_all, Category, User
import admin
from config import MyApp

app = MyApp.app
database = MyApp.database
babel = MyApp.babel
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(user_id):
    return database.session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return login()


@babel.localeselector
def get_locale():
    return "ru"


@app.route("/todo/add", methods=["POST"])
@login_required
def add_todo():
    day_id = request.form.get("day_id")
    name = request.form.get("name")
    end_time = request.form.get("end_time")
    category_id = request.form.get("category_id")
    if end_time == "":
        end_time = None
    else:
        end_time = datetime.strptime(end_time, "%H:%M").time()
    Todo.add(name, day_id, end_time, category_id=category_id)
    return index()


@app.route("/todo/complete", methods=["POST"])
@login_required
def complete_todo():
    todo_id = request.form.get("todo_id")
    todo = find_by_id(todo_id, Todo)
    todo.open = False
    save(todo)
    return index()


@app.route("/todo/delete", methods=["POST"])
@login_required
def delete_todo():
    todo_id = request.form.get("todo_id")
    todo = find_by_id(todo_id, Todo)
    delete(todo)
    return index()


@app.route("/category/add", methods=["POST"])
@login_required
def add_category():
    name = request.form.get("name")
    Category.add(name, current_user)
    return categories()


@app.route("/week/copy", methods=["POST"])
@login_required
def copy_week():
    week_id = request.form.get("week_id")
    week = find_by_id(week_id, Week)
    current_week = current_user.get_current_week()
    if week != current_week:
        for i in range(7):
            for todo in week.days[i].todos:
                current_week.days[i].todos.append(Todo(name=todo.name, category_id=todo.category_id ))
        save(current_week)
    return profile()


@app.route("/week/<week_id>/show")
@login_required
def show_week(week_id):
    return index(week_days=find_by_id(int(week_id), Week).get_week_days())


@app.route("/categories")
@login_required
def categories():
    return render_template("categories.html", categories=get_all(Category))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.find_by_username(username)
        if user and user.check_password(password):
            login_user(user, remember=True)
            return index()
    return render_template("login.html")


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        user = User.find_by_username(username)
        if user is None and password == password_again:
            user = User(username=username)
            user.set_password(password)
            save(user)
            login_user(user, remember=True)
            return index()
    return render_template("registration.html")


@app.route("/report")
@login_required
def report():
    filename = f"{datetime.now().date()}.html"
    with open(f"reports/{filename}", "w", encoding=MyApp.ENCODING) as file:
        file.write(render_template("report.html", current_user=current_user))
    return send_from_directory("reports", filename, as_attachment=True)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/")
@login_required
def index(week_days=None):
    if week_days is None:
        week_days = current_user.get_current_week().get_week_days()
    return render_template("index.html", user=current_user, week_days=week_days)


if __name__ == '__main__':
    database.create_all()
    admin.config()
    app.run()
