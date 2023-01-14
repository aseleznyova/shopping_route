import json
from flask import request
from __init__ import create_app
import database
from models import Product

app = create_app()

@app.route('/', methods=['GET'])
def fetch():
    products = database.get_all(Product)
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

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    name = data['name']
    price = data['price']
    weight = data['weight']

    database.add_instance(Product, name=name, price=price, weight=weight)
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
