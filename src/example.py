from core.models import Database

database = Database()

resultado = database.get_by_name("%Diego%")




print(resultado)