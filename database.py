import sqlalchemy

# Conexión a BD postgres en localhost
# con usuario cocollector
# y contraseña 12345678
db = sqlalchemy.create_engine("postgresql+psycopg2://cocollector:12345678@localhost/BDCocoProyecto")

db.connect()

print (db)
