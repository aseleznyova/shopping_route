import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    stores_products = db.relationship('StoresProduct', lazy='select',
        backref=db.backref('products', lazy='joined'))

class Stores(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    stores_products = db.relationship('StoresProduct', lazy='select',
        backref=db.backref('stores', lazy='joined'))
    points_store = db.relationship('PointsStores', lazy='select',
        backref=db.backref('stores', lazy='joined'))

class StoresProduct(db.Model):
    __tablename__ = 'stores_product'
    stores_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    price = db.Column(db.Float)

class StoresDistance(db.Model):
    __tablename__ = 'stores_distance'
    stores_id1 = db.Column(db.Integer, db.ForeignKey('points_stores.id', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    stores_id2 = db.Column(db.Integer, db.ForeignKey('points_stores.id', ondelete='CASCADE'), nullable=False, index=True, primary_key=True)
    distance = db.Column(db.Float)
    
class PointsStores(db.Model):
    __tablename__ = 'points_stores'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stores_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), nullable=False, index=True)
    #store_distance = db.relationship('StoresDistance', lazy='select',
       # backref=db.backref('points_stores', lazy='joined'))