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
                ft.DataCell(ft.Text(name, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1), on_tap=lambda e, id=id: toggle_checkbox(e, id)),
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
            column.controls = [titulo, row_nombre, results_container]
            page.update()
            
        elif selection.value == "Código":
            column.controls = [titulo, row_codigo, results_container]
            page.update()


    # tabla para mostrar resultados de búsqueda (se actualiza en vivo)
    resultados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Seleccionar")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Cinturón")),
            ft.DataColumn(ft.Text("Rango")),
            ft.DataColumn(ft.Text("Código")),
        ],
        rows=[],
        expand=True,
        
    )

    # contenedor para alinear el DataTable en la parte superior y quitar margen
    results_container = ft.Container(resultados,
                                    alignment=ft.alignment.top_center,
                                    padding=0,
                                    margin=ft.margin.only(top=0),
                                    expand=True)

    def actualizar_resultados(rows_data):
        rows = []
        for id, name, age, kyu in rows_data:
            age = resources.calcular_edad(age)
            cinta = resources.num_to_cinta(kyu)
            rango = resources.num_to_rango(kyu)

            checkbox = ft.Checkbox(data=id)
            row = ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),
                    ft.DataCell(ft.Text(name, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1)),
                    ft.DataCell(ft.Text(age)),
                    ft.DataCell(ft.Text(cinta)),
                    ft.DataCell(ft.Text(rango)),
                    ft.DataCell(ft.Text(id)),
                ],
            )
            rows.append(row)
        resultados.rows = rows
        resultados.update()
        page.update()

    def buscar_nombre(e):
        # obtener valor desde el evento (on_change) o desde el TextField (on_click)
        if hasattr(e, "control") and getattr(e.control, "value", None) is not None:
            val = e.control.value if getattr(e.control, "value", None) is not None else ""
        else:
            val = nombre.value if nombre is not None else ""
        q = (val or "").strip()
        if q == "":
            resultados.rows = []
            resultados.update()
            return
        rows_data = db.get_by_name(q)
        actualizar_resultados(rows_data)

    def buscar_codigo(e):
        # obtener valor desde el evento (on_change) o desde el TextField (on_click)
        if hasattr(e, "control") and getattr(e.control, "value", None) is not None:
            # en on_change, e.control es el TextField; en on_click, e.control es el botón
            if hasattr(e.control, "value"):
                val = e.control.value
            else:
                val = codigo.value if codigo is not None else ""
        else:
            val = codigo.value if codigo is not None else ""
        q = (val or "").strip()
        if q == "":
            resultados.rows = []
            resultados.update()
            return
        if resources.comprobar_entero(q):
            rows_data = db.get_by_id(int(q))
            actualizar_resultados(rows_data)
        else:
            boton_edad.color = "red"
            boton_edad.update()

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


    selection = metodo()

    codigo = ft.TextField(label="Código", hint_text="Ingrese el código del alumno", on_change=buscar_codigo)
    boton_edad = ft.ElevatedButton(text="Buscar", on_click=buscar_codigo)

    nombre = ft.TextField(label="Nombre", hint_text="Ingrese el nombre del alumno", on_change=buscar_nombre)
    boton_nombre = ft.ElevatedButton(text="Buscar", on_click=buscar_nombre)
    

    row_nombre = ft.Row(
        controls=[
            selection,
            nombre,
            boton_nombre
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=False,)
    
    row_codigo = ft.Row(
        controls=[
            selection,
            codigo,
            boton_edad
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=False,)


    column = ft.Column(
        controls=[
            titulo,
            selection,
        ],
        spacing=0,
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

    titulo = ft.Text(value="Filtrar",
                     size=30,
                     text_align=ft.TextAlign.CENTER)
    
    # tabla para mostrar resultados de filtrado (se actualiza en vivo)
    resultados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Seleccionar")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Cinturón")),
            ft.DataColumn(ft.Text("Rango")),
            ft.DataColumn(ft.Text("Código")),
        ],
        rows=[],
        expand=True,
    )

    # contenedor para alinear el DataTable en la parte superior y quitar margen
    results_container = ft.Container(resultados,
                                    alignment=ft.alignment.top_center,
                                    padding=0,
                                    margin=ft.margin.only(top=0),
                                    expand=True)

    def actualizar_resultados(rows_data):
        rows = []
        for id, name, age, kyu in rows_data:
            age = resources.calcular_edad(age)
            cinta = resources.num_to_cinta(kyu)
            rango = resources.num_to_rango(kyu)

            checkbox = ft.Checkbox(data=id)
            row = ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),
                    ft.DataCell(ft.Text(name, overflow=ft.TextOverflow.ELLIPSIS, max_lines=1)),
                    ft.DataCell(ft.Text(age)),
                    ft.DataCell(ft.Text(cinta)),
                    ft.DataCell(ft.Text(rango)),
                    ft.DataCell(ft.Text(id)),
                ],
            )
            rows.append(row)
        resultados.rows = rows
        resultados.update()
        page.update()

    def on_change(e):
        if selection.value == "Cinta":
            column.controls = [titulo, row_cinta, results_container]
            page.update()
            
        elif selection.value == "Edad":
            column.controls = [titulo, row_edad, results_container]
            page.update()

    def metodo():
        selection = ft.Dropdown(label="Filtrar por: ",
                                hint_text="seleccione algo...",
                                options=[
                                    ft.dropdown.Option("Cinta"),
                                    ft.dropdown.Option("Edad"),
                                ],
                                text_align=ft.TextAlign.CENTER,
                                expand=False,
                                width=200,
                                on_change=on_change)
                                
        return selection
        
    def filtrar_cinta(e):
        # obtener valor desde el evento (on_change) o desde el Dropdown/Checkbox
        val = None
        if hasattr(e, "control"):
            ctrl = e.control
            # si el control es el Checkbox, su .value es bool; en ese caso tomamos el valor del Dropdown
            if getattr(ctrl, "value", None) is not None and not isinstance(ctrl.value, bool):
                val = ctrl.value
        if val is None:
            val = cinta_select.value if cinta_select is not None else ""
        q = (str(val) or "").strip()
        # normalizar a minúsculas para comparar con canonical_color
        q_norm = q.lower()
        # estado del checkbox 'Con rallita'
        con_ralla = bool(getattr(con_rallita, "value", False))
        if q == "":
            resultados.rows = []
            resultados.update()
            return
        # filtrar por cinta consultando todos y comparando color base y presencia de rallita
        rows_all = db.fetch_all()
        filtered = []
        for r in rows_all:
            cinta = resources.num_to_cinta(r[3])
            base = resources.canonical_color(cinta)
            has_ralla = resources.cinta_has_ralla(cinta)
            if base == q_norm and (has_ralla if con_ralla else not has_ralla):
                filtered.append(r)
        actualizar_resultados(filtered)

    def filtrar_edad(e):
        # obtener valor desde el evento (on_change) o desde el TextField
        if hasattr(e, "control") and getattr(e.control, "value", None) is not None:
            val = e.control.value if getattr(e.control, "value", None) is not None else ""
        else:
            val = edad.value if edad is not None else ""
        q = (val or "").strip()
        if q == "":
            resultados.rows = []
            resultados.update()
            return
        if resources.comprobar_entero(q):
            # filtrar por edad calculada
            rows_all = db.fetch_all()
            filtered = [r for r in rows_all if int(resources.calcular_edad(r[2])) == int(q)]
            actualizar_resultados(filtered)
        else:
            boton_edad.color = "red"
            boton_edad.update()

    selection = metodo()

    edad = ft.TextField(label="Edad", hint_text="Ingrese la edad del alumno", on_change=filtrar_edad)
    boton_edad = ft.ElevatedButton(text="Filtrar", on_click=filtrar_edad)

    con_rallita = ft.Checkbox(label="Con rallita", value=False, on_change=filtrar_cinta)
    # mostrar colores en Title Case para mejor presentación (p. ej. 'Blanco')
    cinta_select = ft.Dropdown(label="Cinta", hint_text="Seleccione un color",
                               options=[ft.dropdown.Option(c.title()) for c in resources.get_colors()],
                               on_change=filtrar_cinta,
                               expand=False,
                               width=250)
    boton_cinta = ft.ElevatedButton(text="Filtrar", on_click=filtrar_cinta)
    

    row_cinta = ft.Row(
        controls=[
            selection,
            cinta_select,
            con_rallita,
            boton_cinta
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=False,)
    
    row_edad = ft.Row(
        controls=[
            selection,
            edad,
            boton_edad
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=False,)


    column = ft.Column(
        controls=[
            titulo,
            selection,
        ],
        spacing=0,
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

