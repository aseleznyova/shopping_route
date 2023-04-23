from models import Products, Stores, StoresProduct, PointsStores, StoresDistance
from init import get_dist
import numpy as np
from aco import AntColony
from pack import product
import sys

def calculate_solution(data):
    stores, product_list = create_product_list(data['list_products'])
    dist = create_dist_graph(data['coordinates'], stores)
    #запускаем алгоритм возвращаем pack obj
    #print(stores, product_list, dist, file=sys.stderr)
    ant_colony = AntColony(dist, 10, 3, 100, 0.95, product_list, float(data['time'])*60, float(data['weight'])*1000, alpha=1, beta=1)
    pack = ant_colony.run()
    #shortest_path = pack
    #print("pack", file=sys.stderr)
    ##for k, v in shortest_path.plan.items():
    #   print("node", k, "products:", v, file=sys.stderr)
    #print("time:", shortest_path.path_time, "path:", shortest_path.cur_tour, file=sys.stderr)
    #print("path_lenght", shortest_path.lenght_tour, file=sys.stderr)
    return pack_to_json(pack, stores, data['coordinates'])

def pack_to_json(pack, stores, coordinates):
    response = dict()
    response['costs'] = pack.price
    response['time'] = float(pack.path_time/60)
    points_route = []
    shopping_cart = []
    if len(pack.cur_tour):
        points_route.append(coordinates)
        for i in range(1, len(pack.cur_tour)):
            points_route.append({
                'longitude' : stores[pack.cur_tour[i][0]].longitude,
                'latitude' : stores[pack.cur_tour[i][0]].latitude
            })
            for product_store in range(len(pack.plan[pack.cur_tour[i][0]])):
               shopping_cart.append({
                   'address' : stores[pack.cur_tour[i][0]].address,
                   'name' : Products.query.filter_by(id=pack.plan[pack.cur_tour[i][0]][product_store][0]).first().name,
                   'price' : pack.plan[pack.cur_tour[i][0]][product_store][1]
               }) 
        points_route.append(coordinates)
    response['route'] = points_route
    response['shopping_cart'] = shopping_cart
    return response


    
def create_dist_graph(coordinates, stores):
    dist = np.full((len(stores)+1,len(stores)+1), np.inf)
    #вычисляем растояния между point и магазинами которые, есть в списке stores
    for i in range(len(dist)):
        for j in range(len(dist[i])):
            if i > j:
                dist[i][j] = dist[j][i]
            elif i == j:
                continue
            elif i == 0:
                dist[i][j] = get_dist(coordinates['longitude'], coordinates['latitude'],
                                      stores[j].longitude, stores[j].latitude)
            else:
                distance = StoresDistance.query.filter_by(stores_id1=stores[i].id,stores_id2=stores[j].id).first()
                if not distance:
                    distance = StoresDistance.query.filter_by(stores_id1=stores[j].id,stores_id2=stores[i].id).first()
                print(stores[i].id, stores[j].id, file=sys.stderr)
                dist[i][j] = distance.distance
    return dist


def create_product_list(products):
    stores = dict()
    points = dict()
    product_list = []
    for item in products:
        product_from_db = Products.query.filter_by(id=item['id'],name=item['name']).first()
        if product_from_db:
            list_stores_with_product = StoresProduct.query.filter_by(products_id=product_from_db.id).all()
            for store in list_stores_with_product:
                list_points_store = PointsStores.query.filter_by(stores_id = store.stores_id).all()
                for point in list_points_store:
                    if point.id not in points:
                        points[point.id] = len(stores)+1
                        stores[len(stores)+1] = point
                    product_list.append(product(weight=product_from_db.weight,
                                                price=store.price, store=points[point.id],
                                                pid=product_from_db.id))
    return stores, product_list
