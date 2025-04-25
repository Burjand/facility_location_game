import networkx as nx
import random
import numpy as np

class FLG_environment:

    def __init__(self, n_nodes, potential_facilities, seed=42, demand_distribution=('normal',20,5), weight_distribution=('normal',5,1)):
        
        self.n_nodes = n_nodes
        self.seed = seed
        self.demand_distribution = demand_distribution
        self.weight_distribution = weight_distribution
        self.potential_facilities = potential_facilities

        self.check_potential_facilities()
        self.FLG_env = self.generate_flg_env()


    def check_potential_facilities(self):

        if self.potential_facilities > self.n_nodes:
            raise ValueError("Number of potential facilities cannot exceed number of nodes.")
        if self.potential_facilities < 1:
            raise ValueError("Number of potential facilities must be at least 1.")
        return 0
    

    def generate_flg_env(self):

        base_tree = self.generate_tree()
        node_demand = self.generate_demand_distribution()
        potential_facilities = self.select_potential_facilities()

        return (base_tree, node_demand, potential_facilities)

    
    def generate_tree(self):

        random.seed(self.seed)
        G = nx.Graph()
        nodes = list(range(self.n_nodes))
        G.add_node(nodes[0])
        
        if self.weight_distribution[0] == 'normal':
            for i in nodes[1:]:
                parent = random.choice(nodes[:i])
                random_weight = np.random.normal(loc=self.weight_distribution[1], scale=self.weight_distribution[2])
                random_weight = np.round(np.abs(random_weight)).astype(int)
                random_weight = np.clip(random_weight,1,None)
                G.add_edge(parent, i, weight=random_weight)
        elif self.weight_distribution[0] == 'uniform':
            for i in nodes[1:]:
                parent = random.choice(nodes[:i])
                random_weight = np.random.uniform(low=self.weight_distribution[1], high=self.weight_distribution[2])
                random_weight = np.round(np.abs(random_weight)).astype(int)
                random_weight = np.clip(random_weight,1,None)
                G.add_edge(parent, i, weight=random_weight)
        else:
            raise ValueError("Unsupported weight distribution type.")

        G_adj_matrix = np.array(nx.adjacency_matrix(G).todense())
        
        return G_adj_matrix
    

    def generate_demand_distribution(self):

        if self.demand_distribution[0] == 'normal':
            demand = np.random.normal(loc=self.demand_distribution[1], scale=self.demand_distribution[2], size=self.n_nodes)
        elif self.demand_distribution[0] == 'uniform':
            demand = np.random.uniform(low=self.demand_distribution[1], high=self.demand_distribution[2], size=self.n_nodes)
        else:
            raise ValueError("Unsupported demand distribution type.")
        
        demand = np.round(np.abs(demand)).astype(int)
        demand = np.clip(demand,1,None)

        return demand
    

    def select_potential_facilities(self):

        arr = np.zeros(self.n_nodes, dtype=int)
        arr[:self.potential_facilities] = 1
        np.random.shuffle(arr)
        return arr.tolist()
        
        return selected_nodes