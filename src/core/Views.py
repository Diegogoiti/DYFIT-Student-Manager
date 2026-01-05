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
        # obtener control del checkbox si viene del on_change
        checkbox = None
        if hasattr(e, "control") and getattr(e.control, "data", None) is not None:
            checkbox = e.control
            self.seleccionado[id] = checkbox
        else:
            checkbox = self.seleccionado.get(id)

        if id in self.selected_ids:
            self.selected_ids.remove(id)
            if checkbox is not None:
                checkbox.value = False
                checkbox.update()
        else:
            self.selected_ids.add(id)
            if checkbox is not None:
                checkbox.value = True
                checkbox.update()
        page.update()
        


    def reset_selections(e):
        # desmarca todos los checkboxes guardados y limpia el set de seleccion
        for _id, checkbox in list(self.seleccionado.items()):
            try:
                checkbox.value = False
                checkbox.update()
            except Exception:
                pass
        self.selected_ids.clear()
        page.update()

    students_data = db.fetch_all()

    rows = []
    for id, name, age, kyu in students_data:
        age = resources.calcular_edad(age)
        cinta = resources.num_to_cinta(kyu)
        rango = resources.num_to_rango(kyu)

        checkbox = ft.Checkbox(data=id, value=(id in self.selected_ids), on_change=lambda e, id=id: toggle_checkbox(e, id))
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
    
    boton_reiniciar = ft.ElevatedButton(text="Reiniciar selecciones", on_click=reset_selections)

    column.controls = [titulo, ft.Row([boton_reiniciar], alignment=ft.MainAxisAlignment.END), table]
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
    db = models.Database()

    titulo = ft.Text(value="Ingresar alumno", size=30, text_align=ft.TextAlign.CENTER)

    nombre = ft.TextField(label="Nombre", width=250)
    fecha = ft.TextField(label="Fecha de nacimiento", hint_text="DD/MM/YYYY", width=250)

    # dropdown de cintas + checkbox rallita
    # el Dropdown es más estrecho para dejar espacio al checkbox al lado
    cinta_select = ft.Dropdown(label="Cinta", hint_text="Seleccione un color",
                               options=[ft.dropdown.Option(c.title()) for c in resources.get_colors()],
                               expand=False,
                               width=180)
    con_rallita = ft.Checkbox(label="Con rallita", value=False)
    dan_field = ft.TextField(label="Dan", hint_text="1", width=80, visible=False)

    mensaje = ft.Text("")

    def on_cinta_change(e):
        val = (e.control.value or "").strip() if hasattr(e, "control") and getattr(e.control, "value", None) is not None else (cinta_select.value or "")
        is_negro = val.lower() == "negro"
        dan_field.visible = is_negro
        con_rallita.visible = not is_negro
        dan_field.update()
        con_rallita.update()
        page.update()

    cinta_select.on_change = on_cinta_change

    def submit(e):
        n = (nombre.value or "").strip()
        f = (fecha.value or "").strip()
        c = (cinta_select.value or "").strip()
        ralla = bool(getattr(con_rallita, "value", False))
        if not n or not f or not c:
            mensaje.value = "Complete todos los campos"
            mensaje.color = "red"
            mensaje.update()
            return
        # validar fecha
        try:
            _ = resources.calcular_edad(f)  # lanzará si formato inválido
        except Exception:
            mensaje.value = "Fecha inválida (DD/MM/YYYY)"
            mensaje.color = "red"
            mensaje.update()
            return
        # si es negro, usar campo Dan
        if c.lower() == "negro":
            d = (dan_field.value or "").strip()
            if not d or not resources.comprobar_entero(d) or int(d) < 1:
                mensaje.value = "Ingrese un número de Dan válido (1,2,...)"
                mensaje.color = "red"
                mensaje.update()
                return
            rv = float(1 - int(d))
        else:
            # convertir color+ralla a rango
            rv = resources.color_ralla_to_range(c.lower(), ralla)
        ok = db.set(n, f, rv)
        if ok:
            mensaje.value = "Alumno ingresado"
            mensaje.color = "green"
            mensaje.update()
            # volver a consulta y refrescar
            self.update_view(consulta(self, page))
        else:
            mensaje.value = "Error al ingresar"
            mensaje.color = "red"
            mensaje.update()

    boton = ft.ElevatedButton(text="Ingresar", on_click=submit)

    # alinear el row de cinta dentro de un container del mismo ancho que los campos
    cinta_row = ft.Container(ft.Row([cinta_select, dan_field, con_rallita], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER), width=250)

    form = ft.Column([titulo, nombre, fecha, cinta_row, boton, mensaje], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    return ft.Container(form, padding=10, alignment=ft.alignment.top_center, expand=True)


def actualizar(self: "MyApp", page: ft.Page):
    db = models.Database()
    ids = list(self.selected_ids)

    titulo = ft.Text(value="Actualizar alumno", size=30, text_align=ft.TextAlign.CENTER)
    mensaje = ft.Text("")

    if len(ids) != 1:
        info = ft.Text("Seleccione exactamente 1 alumno para actualizar.")
        boton_volver = ft.ElevatedButton(text="Volver", on_click=lambda e: self.update_view(consulta(self, page)))
        col = ft.Column([titulo, info, boton_volver, mensaje], spacing=10)
        return ft.Container(col, padding=10, alignment=ft.alignment.top_center, expand=True)

    id_ = ids[0]
    row = db.get_by_id(int(id_))
    if not row:
        mensaje.value = "Alumno no encontrado"
        mensaje.color = "red"
        mensaje.update()
        return ft.Container(ft.Column([titulo, mensaje]), padding=10, alignment=ft.alignment.top_center, expand=True)
    id_f, nombre_v, fecha_v, rango_v = row[0]

    nombre = ft.TextField(label="Nombre", value=nombre_v, width=250)
    fecha = ft.TextField(label="Fecha de nacimiento", value=fecha_v, width=250)
    # rango como dropdown + checkbox
    base_color = resources.canonical_color(resources.num_to_cinta(rango_v)).title()
    has_ralla = resources.cinta_has_ralla(resources.num_to_cinta(rango_v))
    # dropdown más estrecho para espacio al checkbox
    cinta_select = ft.Dropdown(label="Cinta", hint_text="Seleccione un color",
                               options=[ft.dropdown.Option(c.title()) for c in resources.get_colors()],
                               value=base_color,
                               expand=False,
                               width=180)
    con_rallita = ft.Checkbox(label="Con rallita", value=has_ralla)
    # dan field, visible sólo si la cinta es Negro
    dan_field = ft.TextField(label="Dan", hint_text="1", width=80, visible=(base_color.lower()=="negro"))

    def on_cinta_change_update(e):
        val = (e.control.value or "").strip() if hasattr(e, "control") and getattr(e.control, "value", None) is not None else (cinta_select.value or "")
        is_negro = val.lower() == "negro"
        dan_field.visible = is_negro
        con_rallita.visible = not is_negro
        dan_field.update()
        con_rallita.update()
        page.update()

    cinta_select.on_change = on_cinta_change_update

    def submit(e):
        n = (nombre.value or "").strip()
        f = (fecha.value or "").strip()
        c = (cinta_select.value or "").strip()
        ralla = bool(getattr(con_rallita, "value", False))
        if not n or not f or not c:
            mensaje.value = "Complete todos los campos"
            mensaje.color = "red"
            mensaje.update()
            return
        try:
            _ = resources.calcular_edad(f)
        except Exception:
            mensaje.value = "Fecha inválida"
            mensaje.color = "red"
            mensaje.update()
            return
        if c.lower() == "negro":
            d = (dan_field.value or "").strip()
            if not d or not resources.comprobar_entero(d) or int(d) < 1:
                mensaje.value = "Ingrese un número de Dan válido (1,2,...)"
                mensaje.color = "red"
                mensaje.update()
                return
            rv = float(1 - int(d))
        else:
            rv = resources.color_ralla_to_range(c.lower(), ralla)
        ok = db.update_by_id(int(id_), n, f, rv)
        if ok:
            mensaje.value = "Alumno actualizado"
            mensaje.color = "green"
            mensaje.update()
            # refrescar consulta
            self.update_view(consulta(self, page))
        else:
            mensaje.value = "Error al actualizar"
            mensaje.color = "red"
            mensaje.update()

    boton = ft.ElevatedButton(text="Actualizar", on_click=submit)
    cinta_row = ft.Container(ft.Row([cinta_select, dan_field, con_rallita], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER), width=250)
    col = ft.Column([titulo, nombre, fecha, cinta_row, boton, mensaje], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    return ft.Container(col, padding=10, alignment=ft.alignment.top_center, expand=True)


def borrar(self: "MyApp", page: ft.Page):
    db = models.Database()
    ids = list(self.selected_ids)

    titulo = ft.Text(value="Borrar alumnos", size=30, text_align=ft.TextAlign.CENTER)

    if not ids:
        info = ft.Text("No hay alumnos seleccionados para borrar.")
        boton_volver = ft.ElevatedButton(text="Volver", on_click=lambda e: self.update_view(consulta(self, page)))
        return ft.Container(ft.Column([titulo, info, boton_volver]), padding=10, alignment=ft.alignment.top_center, expand=True)

    # mostrar lista resumida
    rows = db.fetch_all()
    selected_rows = [r for r in rows if r[0] in ids]
    lista = ft.Column([ft.Text(f"{r[0]} - {r[1]}") for r in selected_rows])

    mensaje = ft.Text("")

    def confirmar(e):
        for id_ in ids:
            db.delete_by_id(int(id_))
            # eliminar referencias de checkbox si existen
            if id_ in self.seleccionado:
                try:
                    del self.seleccionado[id_]
                except Exception:
                    pass
        # limpiar selección
        self.selected_ids.clear()
        mensaje.value = "Alumnos borrados"
        mensaje.color = "green"
        mensaje.update()
        # volver a consulta
        self.update_view(consulta(self, page))

    boton_confirm = ft.ElevatedButton(text="Confirmar borrado", bgcolor="red", color="white", on_click=confirmar)
    boton_cancel = ft.ElevatedButton(text="Cancelar", on_click=lambda e: self.update_view(consulta(self, page)))

    col = ft.Column([titulo, lista, ft.Row([boton_confirm, boton_cancel]), mensaje], spacing=10)
    return ft.Container(col, padding=10, alignment=ft.alignment.top_center, expand=True)

