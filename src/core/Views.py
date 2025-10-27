import flet as ft
from . import resources
from . import models
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app import MyApp


def consulta(self: "MyApp" , page: ft.Page):
    
    
    db = models.Database()

    

    titulo = ft.Text(value="Consulta",
                     size=30,
                     text_align=ft.TextAlign.CENTER)

    

    column_table = [
        ft.DataColumn(ft.Text("Seleccionar")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Edad")),
        ft.DataColumn(ft.Text("Cinturón")),
        ft.DataColumn(ft.Text("Rango")),
        ft.DataColumn(ft.Text("Código"))
    ]

    

    """tengo una idea para hacer que con un click largo se edite una celda, ya funciona la seleccion aunque no me gusta el efecto que hace"""

    #checkbox_states = {}

    def toggle_checkbox(e, id):
        checkbox = self.seleccionado[id]
        checkbox.value = not checkbox.value
        checkbox.update()


    students_data = db.fetch_all()

    rows = []
    for id, name, age, kyu in students_data:
        age = resources.calcular_edad(age)
        cinta = resources.num_to_cinta(kyu)
        rango = resources.num_to_rango(kyu)

        checkbox = ft.Checkbox(data=id)
        self.seleccionado[id] = checkbox

        row = ft.DataRow(
            cells=[
                ft.DataCell(checkbox),
                ft.DataCell(ft.Text(name), on_tap=lambda e, id=id: toggle_checkbox(e, id)),
                ft.DataCell(ft.Text(age), on_tap=lambda e, id=id: toggle_checkbox(e, id)),
                ft.DataCell(ft.Text(cinta), on_tap=lambda e, id=id: toggle_checkbox(e, id)),
                ft.DataCell(ft.Text(rango), on_tap=lambda e, id=id: toggle_checkbox(e, id)),
                ft.DataCell(ft.Text(id), on_tap=lambda e, id=id: toggle_checkbox(e, id)),
            ],
            
        )
        rows.append(row)

    table = ft.DataTable(
        columns=column_table,
        rows=rows,
        expand=True,
    )

    column = ft.Column(alignment=ft.MainAxisAlignment.START,
                       horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                       expand=True,)
    
    column.controls = [titulo,table]
    container=ft.Container(
        column,
        alignment=ft.alignment.top_center,
        expand=True,
        padding=10,
    )
    
    return container


#comienzo de la vista buscar -------------------------------------------------------------

def buscar(self: "MyApp", page: ft.Page):

    db = models.Database()

    titulo = ft.Text(value="Buscar",
                     size=30,
                     text_align=ft.TextAlign.CENTER)
    
    def on_change(e):
        if selection.value == "Nombre":
            column.controls = [titulo, row_nombre]
            page.update()
            
        elif selection.value == "Código":
            column.controls = [titulo, row_codigo]
            page.update()

    def metodo():
        selection = ft.Dropdown(label="Buscar por: ",
                                hint_text="seleccione algo...",
                                options=[
                                    ft.dropdown.Option("Nombre"),
                                    ft.dropdown.Option("Código"),
                                ],
                                text_align=ft.TextAlign.CENTER,
                                expand=False,
                                width=200,
                                on_change=on_change)
                                
        return selection
        
    def buscar_nombre(e):
        pass

    def buscar_codigo(e):
        if resources.comprobar_entero(codigo.value):
            pass
        else:
            boton_edad.color = "red"
            boton_edad.update()


    selection = metodo()

    codigo = ft.TextField(label="Código", hint_text="Ingrese el código del alumno")
    boton_edad = ft.ElevatedButton(text="Buscar", on_click=buscar_codigo)

    nombre = ft.TextField(label="Nombre", hint_text="Ingrese el nombre del alumno")
    boton_nombre = ft.ElevatedButton(text="Buscar", on_click=buscar_nombre)
    

    row_nombre = ft.Row(
        controls=[
            selection,
            nombre,
            boton_nombre
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,)
    
    row_codigo = ft.Row(
        controls=[
            selection,
            codigo,
            boton_edad
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,)


    column = ft.Column(
        controls=[
            titulo,
            selection,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    container = ft.Container(
        column,
        alignment=ft.alignment.top_center,
        expand=True,
        padding=10,
    )
    
    return container
        


#comienzo de la vista filtrar ----------------------------------------------------


def filtrar(self: "MyApp", page: ft.Page):
    
    db = models.Database()

    titulo = ft.Text(value="Buscar",
                     size=30,
                     text_align=ft.TextAlign.CENTER)
    
    def on_change(e):
        if selection.value == "Nombre":
            column.controls = [titulo, row_nombre]
            page.update()
            
        elif selection.value == "Edad":
            column.controls = [titulo, row_edad]
            page.update()

    def metodo():
        selection = ft.Dropdown(label="Buscar por: ",
                                hint_text="seleccione algo...",
                                options=[
                                    ft.dropdown.Option("cinta"),
                                    ft.dropdown.Option("Edad"),
                                ],
                                text_align=ft.TextAlign.CENTER,
                                expand=False,
                                width=200,
                                on_change=on_change)
                                
        return selection
        
    def filtrar_cinta(e):
        pass

    def filtrar_edad(e):
        if resources.comprobar_entero(edad.value):
            pass
        else:
            boton_edad.color = "red"
            boton_edad.update()

    selection = metodo()

    edad = ft.TextField(label="Edad", hint_text="Ingrese la edad del alumno")
    boton_edad = ft.ElevatedButton(text="Buscar", on_click=filtrar_edad)

    nombre = ft.TextField(label="Nombre", hint_text="Ingrese el nombre del alumno")
    boton_nombre = ft.ElevatedButton(text="Buscar", on_click=filtrar_cinta)
    

    row_nombre = ft.Row(
        controls=[
            selection,
            nombre,
            boton_nombre
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,)
    
    row_edad = ft.Row(
        controls=[
            selection,
            edad,
            boton_edad
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,)


    column = ft.Column(
        controls=[
            titulo,
            selection,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    container = ft.Container(
        column,
        alignment=ft.alignment.top_center,
        expand=True,
        padding=10,
    )
    
    return container

#ingresar-----------------------------------------------------
    
def ingresar(self: "MyApp", page: ft.Page):
    pass

