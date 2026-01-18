import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO
        years,shapes = self._model.populate_dd()
        for year in years:
            option = ft.dropdown.Option(key=year[0], text=year[0])
            self._view.dd_year.options.append(option)
        for shape in shapes:
            option = ft.dropdown.Option(key=shape[0], text=shape[0])
            self._view.dd_shape.options.append(option)

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        self._view.lista_visualizzazione_2.clean()
        year,shape = self._view.dd_year.value,self._view.dd_shape.value
        graph = self._model.create_graph(year,shape)
        self._view.lista_visualizzazione_1.clean()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di vertici: {graph.number_of_nodes()} Numero di archi: {graph.number_of_edges()}'))
        for node in graph.nodes():
            somma = 0
            for neighbor in graph.neighbors(node):
                somma += graph[node][neighbor]['weight']
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Nodo {node.id}, somma pesi su archi = {somma}'))
        self._view.update()

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        path,peso,graph = self._model.get_info()
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Peso cammino massimo: {peso}'))
        for p,w,d in path:
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'{p[0].id} --> {p[1].id}: weight {w} distance {d}'))
        self._view.update()
