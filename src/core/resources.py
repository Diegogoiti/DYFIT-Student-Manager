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
    """Devuelve los colores en el orden solicitado por el usuario."""
    return [
        "blanco",
        "celeste",
        "amarillo",
        "naranja",
        "verde",
        "azul oscuro",
        "marron",
        "negro",
    ]
    