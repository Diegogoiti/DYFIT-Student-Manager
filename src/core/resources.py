import datetime as dt


def comprobar_entero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False
    
def calcular_edad(fecha_de_nacimiento: str) -> str:
    fecha_nacimiento_dt = dt.datetime.strptime(fecha_de_nacimiento, r'%d/%m/%Y')
    fecha_actual = dt.datetime.now()

    # Calcula la diferencia en años
    edad = fecha_actual.year - fecha_nacimiento_dt.year

    # Ajusta la edad si el cumpleaños de este año aún no ha pasado
    if (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento_dt.month, fecha_nacimiento_dt.day):
        edad -= 1

    return str(edad)


def num_to_cinta(rango: float) -> str:
    kyu_to_cinta_map = {
        # Kyu Enteros
        1: 'Marrón',
        2: 'Marrón',
        3: 'Marrón',
        4: 'Azul oscuro',
        5: 'Azul oscuro',
        6: 'Verde',
        7: 'Naranja',
        8: 'Amarillo',
        9: 'Azul Celeste',
        10: 'Blanco',

        # Kyu Flotantes (con ralla según tus ejemplos y las reglas)
        1.5: 'Marrón',
        2.5: 'Marrón',  # Manteniendo ralla explícita si la quieres (según última solicitud)
        3.5: 'Marrón',  # Manteniendo ralla explícita
        4.5: 'Azul oscuro ralla Marrón',
        5.5: 'Azul oscuro', # Manteniendo ralla explícita
        6.5: 'Verde ralla Azul oscuro',
        7.5: 'Naranja ralla Verde',
        8.5: 'Amarillo ralla Naranja',
        9.5: 'Azul Celeste ralla Amarillo',
        10.5: 'Blanco ralla Azul Celeste'
    }

    if rango > 0:
        return kyu_to_cinta_map.get(rango, "Rango no válido")
    else:
        return "Negro"

def num_to_rango(rango: float) -> str:
    if  rango.is_integer() and rango > 0:
        return f"{int(rango)} Kyu"
    elif not rango.is_integer() and rango > 0:
        return f"{int(rango)} Kyu B"
    elif rango <= 0:
        return f"{int(abs(rango) +1)} Dan"
    return "Rango no válido"
        

def get_cintas() -> list[str]:
    """Devuelve una lista ordenada de nombres de cintas disponibles."""
    # iterar sobre los rangos conocidos para obtener nombres únicos
    keys = [10.5,10,9.5,9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,2.5,2,1.5,1,0]
    cintas = {num_to_cinta(k) for k in keys}
    return sorted(cintas)


def cinta_has_ralla(cinta: str) -> bool:
    """Devuelve True si la representación de la cinta indica que tiene 'ralla'."""
    return "ralla" in (cinta or "")


def canonical_color(cinta: str) -> str:
    """Devuelve el nombre canónico del color en minúsculas según las reglas del sistema.
    Resultado en el conjunto: 'blanco', 'celeste', 'amarillo', 'naranja', 'verde', 'azul oscuro', 'marron', 'negro'."""
    s = (cinta or "").lower()
    if "blanco" in s:
        return "blanco"
    if "celeste" in s:
        return "celeste"
    if "amarillo" in s:
        return "amarillo"
    if "naranja" in s:
        return "naranja"
    if "verde" in s:
        return "verde"
    if "azul oscuro" in s:
        return "azul oscuro"
    # cubrir variantes como 'Azul Celeste' -> 'celeste'
    if "azul celeste" in s:
        return "celeste"
    if "marr" in s:  # 'marrón' o 'marron'
        return "marron"
    if "negro" in s:
        return "negro"
    return s


def get_colors() -> list[str]:
    """Devuelve los colores en el orden solicitado por el usuario, incluyendo subrangos.
    Incluye las opciones generales ('marron', 'azul oscuro') y las subopciones detalladas
    como 'marron 1', 'marron 2', 'marron 3', 'azul oscuro 1', 'azul oscuro 2'."""
    return [
        "blanco",
        "celeste",
        "amarillo",
        "naranja",
        "verde",
        
        "azul oscuro 1",
        "azul oscuro 2",
        
        "marron 1",
        "marron 2",
        "marron 3",
        "negro",
    ]
    

def color_ralla_to_range(color: str, con_ralla: bool) -> float:
    """Convierte una combinación color + con_ralla a un valor numérico representativo de rango.
    Interpreta subopciones como 'marron 2' o 'azul oscuro 1'. Si se pasa sólo la base ('marron' o
    'azul oscuro') se devuelve un valor por defecto (marron -> 1.0, azul oscuro -> 5.0).

    Mapeo de subniveles respetando que los kyu son decrecientes:
      - 'marron 1' -> 3.0 (3 Kyu)
      - 'marron 2' -> 2.0 (2 Kyu)
      - 'marron 3' -> 1.0 (1 Kyu)
      - 'azul oscuro 1' -> 5.0 (5 Kyu)
      - 'azul oscuro 2' -> 4.0 (4 Kyu)
    """
    mapping = {
        "blanco": 10.0,
        "celeste": 9.0,
        "amarillo": 8.0,
        "naranja": 7.0,
        "verde": 6.0,
        "azul oscuro": 5.0,
        "marron": 1.0,
        "negro": 0.0,
    }
    base = (color or "").lower().strip()
    # detectar subopciones con número al final: 'marron 2', 'azul oscuro 1', etc.
    parts = base.split()
    number = None
    if parts and parts[-1].isdigit():
        try:
            number = int(parts[-1])
            base_name = " ".join(parts[:-1]).strip()
        except Exception:
            base_name = base
    else:
        base_name = base

    val = mapping.get(base_name, 0.0)

    # si hay número y la base es 'marron' o 'azul oscuro', mapear respetando kyu decrecientes
    if number is not None:
        if base_name == "marron":
            if number == 1:
                val = 3.0
            elif number == 2:
                val = 2.0
            elif number == 3:
                val = 1.0
            else:
                val = mapping.get(base_name, 0.0)
        elif base_name == "azul oscuro":
            if number == 1:
                val = 5.0
            elif number == 2:
                val = 4.0
            else:
                val = mapping.get(base_name, 0.0)

    if con_ralla and base_name != "negro":
        # añadir 0.5 para representar la variante con 'ralla'
        val = val + 0.5
    return float(val)


def rango_to_color_option(rango: float) -> str:
    """Dado un valor numérico de rango (ej. 1.0, 1.5, 4.0, 5.0) devuelve la opción
    de dropdown apropiada (en minúsculas). Ejemplos:
      3.0 -> 'marron 1'
      2.0 -> 'marron 2'
      1.0 -> 'marron 3'
      5.0 -> 'azul oscuro 1'
      4.0 -> 'azul oscuro 2'
      6.0 -> 'verde'
    Si no hay correspondencia específica devuelve la base canónica ('marron','azul oscuro',...)."""
    if rango <= 0:
        return "negro"
    base = canonical_color(num_to_cinta(rango))
    n = int(abs(rango))

    # mapear rangos a subopciones respetando que kyu son decrecientes
    if base == "marron":
        if n == 3:
            return "marron 1"
        if n == 2:
            return "marron 2"
        if n == 1:
            return "marron 3"
    if base == "azul oscuro":
        if n == 5:
            return "azul oscuro 1"
        if n == 4:
            return "azul oscuro 2"
    # por defecto devolver la base
    return base
