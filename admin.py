from model import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import MyApp

app = MyApp.app
database = MyApp.database


def config():
    admin = Admin(app, name='TimeBudget', template_mode='bootstrap3')
    admin.add_view(ModelView(Week, database.session, "Неделя"))
    admin.add_view(ModelView(Day, database.session, "День"))
    admin.add_view(ModelView(Todo, database.session, "Задача"))
