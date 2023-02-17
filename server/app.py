import json
from flask import request
from __init__ import create_app
import database
from models import Products, Stores, StoresProduct

app = create_app()

@app.route('/products', methods=['GET'])
def fetch_products():
    products = database.get_all(Products)
    all_products = []
    for product in products:
        new_product = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "weight": product.weight
        }

        all_products.append(new_product)
    return json.dumps(all_products), 200

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data['name']
    price = data['price']
    weight = data['weight']

    database.add_instance(Products, name=name, price=price, weight=weight)
    return json.dumps("Added"), 200

@app.route('/stores', methods=['GET'])
def fetch_stores():
    stores = database.get_all(Stores)
    all_stores = []
    for store in stores:
        new_store = {
            "id": store.id,
            "name": store.name,
            "short_name": store.short_name
        }

        all_stores.append(new_store)
    return json.dumps(all_stores), 200

@app.route('/stores', methods=['POST'])
def add_store():
    data = request.get_json()
    name = data['name']
    short_name = data['short_name']

    database.add_instance(Stores, name=name, short_name=short_name)
    return json.dumps("Added"), 200

@app.route('/product_stores', methods=['GET'])
def fetch_products_stores():
    products_stores = database.get_all(StoresProduct)
    all_products_stores = []
    for products_store in products_stores:
        new_product = {
            "stores_id": products_store.stores_id,
            "products_id": products_store.products_id,
        }

        all_products_stores.append(new_product)
    return json.dumps(all_products_stores), 200

@app.route('/product_stores', methods=['POST'])
def add_products_stores():
    data = request.get_json()
    stores_id = data['stores_id']
    products_id = data['products_id']

    database.add_instance(StoresProduct, stores_id=stores_id, products_id=products_id)
    return json.dumps("Added"), 200


@app.route('/remove/<product_id>', methods=['DELETE'])
def remove(product_id):
    database.delete_instance(Product, id=product_id)
    return json.dumps("Deleted"), 200

@app.route('/edit/<product_id>', methods=['PATCH'])
def edit(product_id):
    data = request.get_json()
    new_price = data['price']
    database.edit_instance(Product, id=product_id, price=new_price)
    return json.dumps("Edited"), 200

if __name__ == "__main__":
    app.run('0.0.0.0', 5001)
