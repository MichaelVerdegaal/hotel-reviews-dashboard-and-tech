###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.database import create_connection

c = create_connection()
db = c.reviews
print(db)

