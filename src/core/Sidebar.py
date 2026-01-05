import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import MyApp


class sidebar:
    def __init__(self, app: "MyApp"): # Añade la anotación de tipo para 'page'
        
        
        button_width = 150
        
        # Define los botones sin comas al final
        self.button_filter = ft.ElevatedButton(
            "Filtrar", 
            icon=ft.Icons.FILTER_ALT, 
            on_click=lambda e: app.set_filtrar(), # Mensaje más específico
            width=button_width
        )
        self.button_search = ft.ElevatedButton(
            "Buscar", 
            icon=ft.Icons.SEARCH, 
            on_click=lambda e: app.set_buscar(), # Mensaje más específico
            width=button_width
        )
        self.button_query = ft.ElevatedButton(
            "Consultar", 
            icon=ft.Icons.DATASET_OUTLINED, 
            on_click=lambda e: app.set_consulta(), # Mensaje más específico
            width=button_width
        )
        
        self.button_set = ft.ElevatedButton(
            "Ingresar", 
            icon=ft.Icons.DATASET, 
            on_click=lambda e: app.set_ingresar(),
            width=button_width
        )
        self.button_update = ft.ElevatedButton(
            "Actualizar", 
            icon=ft.Icons.SYSTEM_UPDATE_ALT, 
            on_click=lambda e: app.set_update(),
            width=button_width
        )
        self.button_delete = ft.ElevatedButton(
            "Borrar", 
            icon=ft.Icons.DELETE, 
            on_click=lambda e: app.set_delete(),
            width=button_width
        )
        
        # Asigna el Container a una propiedad de la instancia (self.content)
        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text("Menú", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        padding=ft.padding.all(10), # Padding específico para el título "Menú"
                        alignment=ft.alignment.center
                    ),
                    ft.Divider(),
                    self.button_filter, # Usa las propiedades de la instancia
                    self.button_search,
                    self.button_query,
                    ft.Divider(),
                    self.button_set,
                    self.button_update,
                    self.button_delete
                ],
                width=200, 
                spacing=10, 
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.all(10), # Padding general para toda la barra lateral
            # No es necesario especificar width aquí si la columna interna ya lo tiene
        )