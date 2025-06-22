from core import models

db = models.Database()
#db.set("Fulano de tal", "27/01/2009", 8.5)
data = db.fetch_all()
alumno = data[0]

id, nombre, fecha_nacimiento, rango = alumno

print(data)

for i in alumno:
    print(i)