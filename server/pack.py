
class product:
    def __init__(self, weight : float, price : float, store : int, pid: int, count:int):
        self.weight = weight
        self.price = price
        self.store = store
        self.pid = pid
        self.count = count

class pack:
    def __init__(self, tour, distance, time_max, weight_max):
        self.products = {}
        self.path_time = 0.0
        self.tour = tour
        self.cur_tour = []
        self.distance = distance
        self.price = 0.0
        self.Vmax = 1.4
        self.Vmin = 0.7
        self.W = weight_max
        self.lenght_tour = 0
        self.current_weight = 0
        self.max_t = time_max
        self.plan = dict()

    def add_product(self, produc : product):
        if produc.pid in self.products:
            save_product = self.products[produc.pid]
            save_price = self.price
            save_time = self.path_time
            self.products[produc.pid] = produc
            self.update_tour()
            if self.path_time > self.max_t:
                self.products[produc.pid] = save_product
                self.update_tour()
                return
            else:
                if self.price < save_price:
                    return
                elif self.price == save_price and self.path_time < save_time:
                    return 
                else:
                    self.products[produc.pid] = save_product
                    self.update_tour()
                    return
        else:
            self.products[produc.pid] = produc
            self.update_tour()
            if self.path_time < self.max_t and self.current_weight < self.W:
                return
            else:
                self.products.pop(produc.pid)
                self.update_tour()
    
    def update_tour(self):
        w = 0.0
        t = 0.0
        price = 0.0
        cur_store = self.tour[0][0]
        tour = []
        lenght_tour=0
        plan = dict()
        for i in range(len(self.tour)):
            new_w = 0.0
            for key, value in self.products.items():
                if value.store == self.tour[i][1]:
                    new_w += value.weight
                    price += value.price
                    if value.store not in plan:
                        plan[value.store] = [value]
                    else:
                        plan[value.store].append(value)
            if new_w:
                t += self.distance[cur_store][self.tour[i][1]]/self.speed(w)
                lenght_tour+=self.distance[cur_store][self.tour[i][1]]
                tour.append((cur_store, self.tour[i][1]))
                cur_store = self.tour[i][1]
                w+=new_w
        if w:
            t+= self.distance[cur_store][self.tour[len(self.tour)-1][1]]/self.speed(w)
            lenght_tour+=self.distance[cur_store][self.tour[len(self.tour)-1][1]]
            tour.append((cur_store, self.tour[len(self.tour)-1][1]))
        self.path_time = t
        self.price = price
        self.cur_tour = tour
        self.plan = plan
        self.current_weight = w
        self.lenght_tour = lenght_tour


    def speed(self, w):
        return self.Vmax - w*((self.Vmax-self.Vmin)/self.W)

    def __lt__(self, other):
        if len(self.products) > len(other.products):
            return False
        elif len(self.products) == len(other.products):
            if self.price < other.price:
                return False
            elif self.path_time < other.path_time:
                return False
            else:
                return True
        else:
            return True
    