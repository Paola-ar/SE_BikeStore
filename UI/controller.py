from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def populate_dd_category(self):
        categories = self._model.get_categories()
        self._view.dd_category.options = [ft.dropdown.Option(key = c.category_name, data = c) for c in categories]
        self._view.update()

    def handle_change_category(self,e):
        selected_key = e.control.value # e.control è il Dropdown che ha generato l'evento
        # se key = "mb" data = l'oggetto categoria
        # se si seleziona mountainbike, e.contro.value = mountain bike

        #scorrimento di tutte opzioni dropdown
        for opt in e.control.options: # tutte opzioni del menu
            if opt.key == selected_key: # se abbiamo trovato l'opzione selezionata
                # recupero l'oggetto category
                self.dd_category_value = opt.data # prendo la data(prima inserito come oggetto) di opt che è selzione corrente = quella selezionata da dd
                break




    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO

        self._model.build_graph(self.dd_category_value, self._view.dp1.value, self._view.dp2.value)
        n_nodes,n_edges = self._model.get_graph_details()
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate: "
                                                         f"\nStart date : {self._view.dp1.value}"
                                                         f"\nEnd date : {self._view.dp2.value}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato: "
                                                         f"\nNumero di nodi : {n_nodes}"
                                                         f"\nNumero di archi : {n_edges} "))
        self._populate_dd_products()
        self._view.update()

    def _populate_dd_products(self):
        all_nodes = self._model.get_all_nodes()
        self._view.dd_prodotto_iniziale.options = [ft.dropdown.Option(key=c.product_name, data=c) for c in all_nodes] # c è oggetto prodotto
        self._view.dd_prodotto_finale.options = [ft.dropdown.Option(key=c.product_name,data= c)for c in all_nodes]
        self._view.update()

    def handle_choice_prods(self,e):
        #e.control è il dropdown
        selected_key = e.control.value

        #recuper l'oggetto product associato
        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_prod_start_value = opt.data
                break

    def handle_choice_prodf(self,e):
        # e.control è il dropdown
        selected_key = e.control.value

        # recuper l'oggetto product associato
        for opt in e.control.options:
            if opt.key == selected_key:
                self.dd_prod_end_value = opt.data
                break

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        best_prodotti = self._model.get_best_prodotti()
        self._view.txt_risultato.controls.append(ft.Text(f"\nI cinque prodotti più venduti sono: "))
        for p in best_prodotti:
            self._view.txt_risultato.controls.append(ft.Text(f"{p[0].product_name} with score {p[1]}"))
        self._view.update()


    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        if self._view.txt_lunghezza_cammino.value == "":
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f"Inserire lunghezza del cammino"))
            self._view.update()
            return
        try:
            lun = int(self._view.txt_lunghezza_cammino.value)
        except ValueError:
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f"Valore inserito non numerico"))
            self._view.update()
            return

        path,score = self._model.get_best_path(lun,self.dd_prod_start_value,self.dd_prod_end_value)
        if len(path)==0:
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text("Nessun cammino trovato"))
            self._view.update()
            return
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Cammino migliore: "))
        for p in path:
            self._view.txt_risultato.controls.append(ft.Text(f"{p}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Score: {score}"))
        self._view.update()