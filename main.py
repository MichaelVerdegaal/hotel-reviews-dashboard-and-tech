###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.database import create_connection, query_all

db = create_connection()
c = query_all(db, 150000)
print(c)

