import networkx as nx
from geopy import distance

from database.dao import DAO
class Model:
    def __init__(self):
        self.state_dict = {}
        self.connection_list = []
        self.G = nx.Graph()

    def populate_dd(self):
        years = DAO.get_years()
        shapes = DAO.get_shapes()
        return years,shapes

    def create_graph(self,year,shape):
        self.G.clear()
        self.state_list = DAO.get_nodes(shape,year)
        for state in self.state_list:
            self.state_dict[state.id] = state
            self.G.add_node(state)
        self.connection_list = DAO.get_edges()
        for n1, n2 in self.connection_list:
            weight = self.state_dict[n1].weight + self.state_dict[n2].weight
            if weight != 0:
                self.G.add_edge(self.state_dict[n1],self.state_dict[n2],weight=weight, distance=distance.geodesic((self.state_dict[n1].lat, self.state_dict[n1].lng), (self.state_dict[n2].lat, self.state_dict[n2].lng)).km)
        return self.G

    def get_max_recursive(self, start, parz, distance_parz, visited):
        if distance_parz > self.peso_tot:
            self.peso_tot = distance_parz
            self.path_max = list(parz)
        for neighbor in self.G.neighbors(start):
            if (start,neighbor) not in visited and (len(parz) == 0 or self.G[parz[-1][0]][parz[-1][1]]['weight'] < self.G[start][neighbor]['weight']):
                parz.append((start,neighbor))
                distance_parz += self.G[start][neighbor]['distance']
                visited.add((start,neighbor))
                self.get_max_recursive(neighbor, parz, distance_parz, visited)
                parz.pop()
                visited.remove((start,neighbor))
                distance_parz -= self.G[start][neighbor]['distance']

    def get_info(self):
        self.peso_tot = 0
        self.path_max = []
        for source in self.G.nodes():
            self.get_max_recursive(source, [], 0, set())
        final_path = []
        for n1, n2 in self.path_max:
            final_path.append([[n1, n2], self.G[n1][n2]['distance'], self.G[n1][n2]['weight']])
        return final_path, self.peso_tot, self.G