import random as rn
import numpy as np
from numpy.random import choice as np_choice
from pack import product, pack
from queue import PriorityQueue
import math

class AntColony:

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, products_store,  alpha=1, beta=1):
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.products_store = products_store

    def run(self):
        count_steps  = 0
        absolute_best_pack = None
        i = 0
        while i < self.n_iterations and count_steps <= 15:
            all_paths = self.gen_all_paths()
            all_packs = []
            for j in range(len(all_paths)):
                best_pack = self.packing_algorithm(all_paths[j], 10)
                all_packs.append(best_pack)
                if not absolute_best_pack or absolute_best_pack < best_pack:
                    absolute_best_pack = best_pack
                    count_steps = 0
            count_steps += 1
            i += 1
            self.spread_pheronome(all_packs, self.n_best)         
            self.pheromone = self.pheromone * self.decay            
        return absolute_best_pack

    def generate_omega_delta_gamma(self):
        n = 3
        target = 10000
        samples = [rn.randrange(100, target + 1) for _ in range(n - 1)] + [0, target]
        samples.sort()
        probs = [b - a for a, b in zip(samples[:-1], samples[1:])]
        return list(map(lambda x:  float(x/10000) , probs))

    def compute_score(self, params: list, prod: product, path):
        d_i = 0
        start = False
        for i in range(len(path)):
            if(path[i][0] == prod.store):
                start = True
            if start:
                d_i += self.distances[path[i][0]][path[i][1]]
        return (math.pow(prod.weight,params[1]))/(math.pow(prod.price,params[0])*math.pow(d_i,params[2]))

    def packing_algorithm(self, tour, ptries):
        best_pack = pack(tour=tour, distance=self.distances, max_t=40.0 )
        trys = 0
        while trys < ptries:
            params = self.generate_omega_delta_gamma()
            new_pack = pack(tour=tour, distance=self.distances, max_t=40.0 )
            score_queue = PriorityQueue()
            for i in range(len(self.products_store)):
                score_queue.put((self.compute_score(params, self.products_store[i], tour), i))
            while not score_queue.empty():
                prod = self.products_store[score_queue.get()[1]]
                new_pack.add_product(prod)
            if best_pack < new_pack:
                best_pack = new_pack
            trys +=1
        return best_pack

        
    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths)
        for pack in sorted_paths[:n_best]:
            path = pack.cur_tour
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append(path)
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))   
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move
    
'''
distances_store = np.array([[np.inf, 7, 8, 4, 5],
                            [7, np.inf, 6, 3, 2],
                            [8, 6, np.inf, 9, 1],
                            [4, 3, 9, np.inf, 2],
                            [5, 2, 1, 2, np.inf]])

products_stores = [product(3.0, 11.0, 1, 0), product(4.0, 12.0, 1, 1), product(7.0, 22.0, 1, 2),
                    product(3.0, 14.0, 2, 0), product(4.0, 15.0, 2, 1), product(7.0, 20.0, 2, 2),
                    product(3.0, 12.0, 3, 0), product(4.0, 11.0, 3, 1), product(7.0, 27.0, 3, 2),
                    product(3.0, 13.0, 4, 0), product(4.0, 17.0, 4, 1), product(7.0, 24.0, 4, 2),
                    ]

ant_colony = AntColony(distances_store, 10, 3, 100, 0.95, products_stores, alpha=1, beta=1)
shortest_path = ant_colony.run()
print("pack")
for k, v in shortest_path.plan.items():
    print("node", k, "products:", v)
print("time:", shortest_path.path_time, "path:", shortest_path.cur_tour)
print("path_lenght", shortest_path.lenght_tour)'''