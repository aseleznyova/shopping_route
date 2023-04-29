import json
from flask import request, session
from flask_cors import CORS
from init import create_app, get_dist
import os
import database
from models import Products, Stores, StoresProduct
from alghorithm_service import calculate_solution
app = create_app()
CORS(app)
@app.route('/products', methods=['GET'])
def fetch_products():
    products = database.get_all(Products)
    all_products = []
    for product in products:
        new_product = {
            "id": product.id,
            "name": product.name,
        }
        all_products.append(new_product)
    return json.dumps(all_products), 200

@app.route('/route', methods=['POST'])
def add_list_proucts():
    data = request.get_json()
    if 'coordinates' not in data or 'list_products' not in data or 'time' not in data or 'weight' not in data:
        return json.dumps('coordinates or a list of products are missing'), 401
    res = calculate_solution(data)
    return json.dumps(res), 201

@app.route('/coordinates', methods=['POST'])
def add_coordinates():
    data = request.get_json()
    session['coordinates'] = {
        'longitude' : data['longitude'],
        'latitude' : data['latitude']
    }
    return json.dumps("Added"), 201

if __name__ == "__main__":
    app.run('0.0.0.0', os.environ['PORT_SERVER_IN'])
