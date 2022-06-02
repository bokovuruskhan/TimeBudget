from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from config import MyApp
from datetime import datetime, timedelta

database = MyApp.database


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(255), unique=True, nullable=False)
    password = database.Column(database.String(255), unique=True, nullable=False)
    weeks = database.relationship("Week",
                                  backref=database.backref("user", lazy=True))
    categories = database.relationship("Category",
                                       backref=database.backref("user", lazy=True))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_my_week_by_id(self, week_id):
        for week in self.weeks:
            if week.id == week_id:
                return week

    def get_current_week(self):
        today = datetime.today().date()
        current_week_start_date = today - timedelta(days=today.weekday())
        for week in self.weeks:
            if week.start_date == current_week_start_date:
                return week
        week = Week(start_date=current_week_start_date, user=self)
        for i in range(7):
            week.days.append(Day(date=current_week_start_date))
            current_week_start_date += timedelta(days=1)
        save(week)
        return self.get_current_week()

    @staticmethod
    def find_by_username(username):
        return database.session.query(User).filter(User.username == username).first()


class Week(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    start_date = database.Column(database.Date, nullable=False)
    days = database.relationship("Day",
                                 backref=database.backref("week", lazy=True))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def get_week_days(self):
        week = {}
        date = self.start_date
        for i in range(7):
            week.update({date: self.days[i]})
            date += + timedelta(days=1)
        return week


class Day(database.Model):
    day_names = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]

    id = database.Column(database.Integer, primary_key=True)
    date = database.Column(database.Date)
    week_id = database.Column(database.Integer, database.ForeignKey('week.id'))
    todos = database.relationship("Todo",
                                  backref=database.backref("day", lazy=True))

    def get_name(self):
        return self.day_names[self.date.weekday()]

    @staticmethod
    def find_by_date(date):
        return database.session.query(Day).filter(Day.date == date).first()


class Category(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    todos = database.relationship("Todo",
                                  backref=database.backref("category", lazy=True))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def get_total_hours_spent(self):
        hours = 0
        for todo in self.todos:
            if todo.end_time is not None:
                hours += todo.end_time.hour
        return hours

    def get_number_completed_todos(self):
        number = 0
        for todo in self.todos:
            if todo.open is False:
                number += 1
        return number

    @staticmethod
    def add(name, user):
        save(Category(name=name, user=user))


class Todo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    open = database.Column(database.Boolean, default=True, nullable=False)
    end_time = database.Column(database.Time, nullable=True)
    day_id = database.Column(database.Integer, database.ForeignKey('day.id'))
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), nullable=False)

    @staticmethod
    def add(name, day_id, end_time, category_id):
        save(Todo(name=name, day_id=day_id, end_time=end_time, category_id=category_id))


def save(obj):
    database.session.add(obj)
    database.session.commit()


def delete(obj):
    database.session.delete(obj)
    database.session.commit()


def get_all(obj_class):
    return database.session.query(obj_class).all()


def find_by_id(obj_id, obj_class):
    return database.session.query(obj_class).filter(obj_class.id == obj_id).first()
