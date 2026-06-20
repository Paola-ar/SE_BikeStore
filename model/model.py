from database.dao import DAO
import networkx as nx
import copy

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self._products = []
        self.id_prod_map = {}



    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        return DAO.get_category()

    def build_graph(self,category, date1,date2):
        self.G.clear()
        self._products = DAO.get_products_by_cat(category)
        for p in self._products:
            self.id_prod_map[p.id] = p

        self.G.add_nodes_from(self._products)

        all_edges = DAO.get_edges(category, date1, date2,self.id_prod_map)
        for e in all_edges:
            self.G.add_edge(e[0],e[1],weight=e[2])

    def get_graph_details(self):
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def get_best_prodotti(self):
        best = []
        for n in self.G.nodes():
            score = 0
            for e_out in self.G.out_edges(n,data=True):
                score += e_out[2]['weight']
            for e_in in self.G.in_edges(n,data=True):
                score -= e_in[2]['weight']

            best.append((n,score))
        best.sort(reverse=True,key=lambda x:x[1]) # peso
        return best[:5]

    def get_all_nodes(self):
        nodes = list(self.G.nodes())
        nodes.sort(key= lambda x:x.product_name)
        return nodes

    def get_best_path(self,lun,start,end):
        self.best_path = []
        self.best_score = 0
        parziale = [start]
        self._ricorsione(parziale,lun,start,end)
        return self.best_path,self.best_score

    def _ricorsione(self,parziale,lun,start,end):
        if len(parziale) == lun:
            if parziale[-1] == end and self._get_score(parziale) > self.best_score:
                self.best_score = self._get_score(parziale)
                self.best_path = copy.deepcopy(parziale)
            return

        for n in self.G.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,lun,start,end)
                parziale.pop()

    def _get_score(self,parziale):
        score = 0
        for i in range (1,len(parziale)):
            score += self.G[parziale[i-1]][parziale[i]]['weight']
        return score
