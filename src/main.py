# main.py
import flet as ft
import core.Sidebar as Sidebar
import core.Views as Views
from core import models as db
#me falta asociar la base de datos a la vista para obtener los datos

class MyApp:
    def __init__(self,page : ft.Page):
        self.title = "DYFIT Student Manager"
        self.page = page
        self.view = Views.consulta(self.page)
        self.sidebar = Sidebar.sidebar(self)
        self.row = ft.Row(alignment=ft.MainAxisAlignment.START, 
                          vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                          expand=True)
        self.row.controls = [self.sidebar.content, self.view]
        self.main_container = ft.Container()
        self.main_container.content = self.row
        

        

    def main(self):
        self.page.title = self.title
        self.page.add(self.row)
        self.page.update()

    def set_consulta(self):
        self.view = Views.consulta(self.page)
        self.row.controls = [self.sidebar.content, self.view]
        self.page.update()

    def set_filtrar(self):
        self.view = Views.filtrar(self.page)
        self.row.controls = [self.sidebar.content, self.view]
        self.page.update()

    def set_buscar(self):
        self.view = Views.buscar(self.page)
        self.row.controls = [self.sidebar.content, self.view]
        self.page.update()


def Run(page: ft.Page):
    MyApp(page).main()


if __name__ == "__main__":
    ft.app(target=Run)