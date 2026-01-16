import networkx as nx

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
            self.G.add_edge(self.state_dict[n1],self.state_dict[n2],weight=self.state_dict[n1].weight + self.state_dict[n2].weight)
        return self.G
