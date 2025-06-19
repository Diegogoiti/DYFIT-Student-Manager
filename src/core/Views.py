import flet as ft
from . import resources
from . import models

def consulta(page: ft.Page):

    db = models.Database()

    titulo = ft.Text(value="Consulta",
                     size=30,
                     text_align=ft.TextAlign.CENTER)
    students_data = [
        {"nombre": "Juan Pérez", "edad": 20, "curso": "Matemáticas"},
        {"nombre": "Ana Gómez", "edad": 22, "curso": "Historia"},
        {"nombre": "Luis Rodríguez", "edad": 21, "curso": "Física"},
        {"nombre": "Sofía López", "edad": 20, "curso": "Química"},
    ]

    column_table = [
        ft.DataColumn(ft.Text("Seleccionar")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Edad")),
        ft.DataColumn(ft.Text("Curso")),
    ]

    
    rows = []
    for id,student in enumerate(students_data): # el enumerate es provicional, para ver como se comporta, despues se coloca el id de la base de datos
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Checkbox(data=id)),
                ft.DataCell(ft.Text(student["nombre"])),
                ft.DataCell(ft.Text(str(student["edad"]))),
                ft.DataCell(ft.Text(student["curso"])),
            ]
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

def buscar(page: ft.Page):

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
                                    ft.dropdown.Option("Nombre"),
                                    ft.dropdown.Option("Edad"),
                                ],
                                alignment=ft.alignment.center,
                                expand=False,
                                width=200,
                                on_change=on_change)
                                
        return selection
        
    def buscar_nombre(e):
        pass

    def buscar_edad(e):
        if resources.comprobar_entero(edad.value):
            pass
        else:
            boton_edad.color = "red"
            boton_edad.update()


    selection = metodo()

    edad = ft.TextField(label="Edad", hint_text="Ingrese la edad del alumno")
    boton_edad = ft.ElevatedButton(text="Buscar", on_click=buscar_edad)

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
        


#comienzo de la vista filtrar ----------------------------------------------------


def filtrar(page: ft.Page):
    
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
                                    ft.dropdown.Option("Nombre"),
                                    ft.dropdown.Option("Edad"),
                                ],
                                alignment=ft.alignment.center,
                                expand=False,
                                width=200,
                                on_change=on_change)
                                
        return selection
        
    def buscar_nombre(e):
        pass

    def buscar_edad(e):
        if resources.comprobar_entero(edad.value):
            pass
        else:
            boton_edad.color = "red"
            boton_edad.update()

    selection = metodo()

    edad = ft.TextField(label="Edad", hint_text="Ingrese la edad del alumno")
    boton_edad = ft.ElevatedButton(text="Buscar", on_click=buscar_edad)

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
    


