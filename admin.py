from model import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import MyApp

app = MyApp.app
database = MyApp.database


def config():
    admin = Admin(app, name='FlaskTemplateApp', template_mode='bootstrap3')
    admin.add_view(ModelView(Parent, database.session, "Родитель"))
    admin.add_view(ModelView(Children, database.session, "Ребенок"))
