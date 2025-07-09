import datetime as dt


def comprobar_entero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False
    
def calcular_edad(fecha_de_nacimiento: str) -> int:
    fecha_nacimiento_dt = dt.datetime.strptime(fecha_de_nacimiento, '%d/%m/%Y')
    fecha_actual = dt.datetime.now()

    # Calcula la diferencia en años
    edad = fecha_actual.year - fecha_nacimiento_dt.year

    # Ajusta la edad si el cumpleaños de este año aún no ha pasado
    if (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento_dt.month, fecha_nacimiento_dt.day):
        edad -= 1

    return edad


def num_to_cinta(rango) -> str:
    kyu_to_cinta_map = {
        # Kyu Enteros
        1.0: 'Marrón',
        2.0: 'Marrón',
        3.0: 'Marrón',
        4.0: 'Azul oscuro',
        5.0: 'Azul oscuro',
        6.0: 'Verde',
        7.0: 'Naranja',
        8.0: 'Amarillo',
        9.0: 'Azul Celeste',
        10.0: 'Blanco',

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

def num_to_rango(rango) -> str:
    if isinstance(rango,int) and rango > 0:
        return f"{rango} Kyu"
    elif isinstance(rango,float) and rango > 0:
        return f"{int(rango)} Kyu B"
    elif rango <= 0:
        return f"{abs(rango) +1} Kyu"
    return "Rango no válido"
        
     