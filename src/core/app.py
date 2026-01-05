import flet as ft

from . import Views 
from . import models as db
from . import Sidebar 


class MyApp:
    def __init__(self,page : ft.Page):
        self.title = "DYFIT Student Manager"
        self.page = page
        self.seleccionado = {}
        self.view = Views.consulta(self, self.page)
        self.sidebar = Sidebar.sidebar(self)
        self.row = ft.Row(alignment=ft.MainAxisAlignment.START, 
                          vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                          expand=True)
        self.row.controls = [self.sidebar.content,ft.VerticalDivider(), self.view]
        self.main_container = ft.Container()
        self.main_container.content = self.row
        

        

    def main(self):
        self.page.title = self.title
        self.page.add(self.row)
        self.page.update()

    def update_view(self, new_view):
            """Método helper para cambiar la vista principal y actualizar la página."""
            self.view = new_view
            # Reemplaza la vista antigua en el Row manteniendo el sidebar y el divisor
            self.row.controls[-1] = self.view 
            self.page.update()

    def set_consulta(self):
        self.update_view(Views.consulta(self, self.page))
        #print(self.seleccionado)

    def set_filtrar(self):
        self.update_view(Views.filtrar(self, self.page))

    def set_buscar(self):
        self.update_view(Views.buscar(self, self.page))
        
    # Agrega los métodos restantes para la barra lateral
    def set_ingresar(self):
        self.update_view(Views.ingresar(self, self.page))
        
 