import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    weight = db.Column(db.Integer)