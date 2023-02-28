import json
from flask import request, session
from __init__ import create_app, get_dist
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
            "weight": product.weight
        }
        all_products.append(new_product)
    return json.dumps(all_products), 200

@app.route('/products', methods=['POST'])
def add_list_proucts():
    data = request.get_json()
    session['list_products'] = []
    for item in data:
        if Products.query.get(item):
            session['list_products'].append(item)
    return json.dumps("Added"), 201

@app.route('/coordinates', methods=['POST'])
def add_coordinates():
    data = request.get_json()
    session['coordinates'] = {
        'longitude' : data['longitude'],
        'latitude' : data['latitude']
    }
    return json.dumps("Added"), 201

@app.route('/coordinates', methods=['DELETE'])
def delete_coordinates():
    data = request.get_json()
    session['coordinates'] = {}
    return json.dumps("Deleted"), 200

@app.route('/products', methods=['DELETE'])
def delete_list_proucts():
    session['list_products'] = []
    return json.dumps("Deleted"), 200

@app.route('/route', methods=['GET'])
def building_route():
    if 'coordinates' in session and 'list_products' in session:    
        return json.dumps('correct'), 200
    return json.dumps('coordinates or a list of products are missing'), 401


if __name__ == "__main__":
    app.run('0.0.0.0', 5001)
