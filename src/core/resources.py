def comprobar_entero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False