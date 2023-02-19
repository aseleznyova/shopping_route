from flask import Flask

import database
from models import db, Products, Stores, PointsStores, StoresProduct
import config
import pandas as pd

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    if not len(Products.query.all()):
        load_data()
    return flask_app
    
def load_data():
    url_offers = 'https://drive.google.com/file/d/1JYvGQ5HGDCoZK-sUeujOTUz3KvDf0tIq/view?usp=share_link'
    url_stores = 'https://drive.google.com/file/d/1K9f43GcRDoDSQr8lBbgKchEG-2tTApv1/view?usp=share_link'
    url_offers='https://drive.google.com/uc?id=' + url_offers.split('/')[-2]
    url_stores='https://drive.google.com/uc?id=' + url_stores.split('/')[-2]
    df_offers = pd.read_csv(url_offers)
    df_stores = pd.read_csv(url_stores)
    for store in df_stores['name'].unique():
        database.add_instance(Stores, name=store)
        id = Stores.query.filter_by(name=store).all()[0].id
        for i, address in df_stores[df_stores['name'] == store].iterrows():
            database.add_instance(PointsStores, address=address[2], latitude=address[3], longitude=address[4], stores_id=id)
    for index, offers in df_offers.iterrows():
        database.add_instance(Products, name=offers['name'], weight=offers['weight'])
        id_products = Products.query.filter_by(name=offers['name']).all()[0].id
        for store in df_offers.columns[4:]:
            if pd.notna(offers[store]):
                id_store = Stores.query.filter_by(name=store).all()[0].id
                database.add_instance(StoresProduct, stores_id=id_store, products_id=id_products ,price = offers[store])
