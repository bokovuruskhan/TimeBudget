from config import MyApp

database = MyApp.database


class Parent(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    children = database.relationship("Children",
                                     backref=database.backref("parent", lazy=True))

    def __str__(self):
        return self.name


class Children(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    parent_id = database.Column(database.Integer, database.ForeignKey('parent.id'), nullable=True)

    def __str__(self):
        return self.name
