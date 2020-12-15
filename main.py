###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.dashboard import create_worldmap, update_worldmap_settings, create_dash_app
from data.database import *
from data.dataframes import create_marker_label_data

# Data
db = create_connection()
df = query_hotels(db)

# Worldmap
customdata = create_marker_label_data(df)
fig = create_worldmap(df['lat'], df['lng'], customdata)
update_worldmap_settings(fig)

# Dash app
app = create_dash_app(fig)
app.run_server(debug=True)
