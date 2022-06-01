from config import MyApp
from datetime import datetime, timedelta

database = MyApp.database


class Week(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    start_date = database.Column(database.Date, nullable=False)
    days = database.relationship("Day",
                                 backref=database.backref("week", lazy=True))

    @staticmethod
    def find_by_start_date(start_date):
        return database.session.query(Week).filter(Week.start_date == start_date).first()

    @staticmethod
    def init_week():
        today = datetime.today().date()
        current_week_start_date = today - timedelta(days=today.weekday())
        if Week.find_by_start_date(current_week_start_date) is None:
            week = Week(start_date=current_week_start_date)
            for i in range(7):
                week.days.append(Day(date=current_week_start_date))
                current_week_start_date += timedelta(days=1)
            database.session.add(week)
            database.session.commit()

    @staticmethod
    def get_current_week():
        week = {}
        today = datetime.today().date()
        date = today - timedelta(days=today.weekday() + 1)
        for i in range(7):
            date += + timedelta(days=1)
            week.update({date: Day.find_by_date(date)})
        return week


class Day(database.Model):
    day_names = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА", "ВОСКРЕСЕНЬЕ"]

    id = database.Column(database.Integer, primary_key=True)
    date = database.Column(database.Date, unique=True)
    week_id = database.Column(database.Integer, database.ForeignKey('week.id'))
    todos = database.relationship("Todo",
                                  backref=database.backref("day", lazy=True))

    def get_name(self):
        return self.day_names[self.date.weekday()]

    @staticmethod
    def find_by_date(date):
        return database.session.query(Day).filter(Day.date == date).first()


class Todo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    day_id = database.Column(database.Integer, database.ForeignKey('day.id'))

    @staticmethod
    def add(name, day_id):
        database.session.add(Todo(name=name, day_id=day_id))
        database.session.commit()
