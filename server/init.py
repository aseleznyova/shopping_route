from flask import Flask

import database
from models import db, Products, Stores, PointsStores, StoresProduct, StoresDistance
import config
import pandas as pd
import requests
import sys

def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.secret_key = 'super secret key'
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()
    if not len(Products.query.all()):
        load_data()
    return flask_app
    
def get_dist(p1_lon,p1_lat, p2_lon, p2_lat):
    res = requests.request('get','https://routing.openstreetmap.de/routed-foot/route/v1/driving/{},{};{},{}?overview=false&geometries=polyline&steps=true'.format(p1_lon,p1_lat, p2_lon, p2_lat))
    s =res.json()
    #print(s, file=sys.stderr)
    return s['routes'][0]['distance']

def load_data():
    url_offers = 'https://drive.google.com/file/d/1JYvGQ5HGDCoZK-sUeujOTUz3KvDf0tIq/view?usp=share_link'
    url_stores = 'https://drive.google.com/file/d/1K9f43GcRDoDSQr8lBbgKchEG-2tTApv1/view?usp=share_link'
    url_offers = 'https://drive.google.com/uc?id=' + url_offers.split('/')[-2]
    url_stores = 'https://drive.google.com/uc?id=' + url_stores.split('/')[-2]
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
        for store in df_offers.columns[3:]:
            if pd.notna(offers[store]):
                id_store = Stores.query.filter_by(name=store).all()[0].id
                database.add_instance(StoresProduct, stores_id=id_store, products_id=id_products ,price = offers[store])
    stores = database.get_all(PointsStores)
    for i in range(len(stores)):
        j = i + 1
        while j < len(stores):
            dist = get_dist(stores[i].longitude, stores[i].latitude, stores[j].longitude, stores[j].latitude)
            database.add_instance(StoresDistance,stores_id1=stores[i].id,stores_id2=stores[j].id, distance=dist)
            j+=1
