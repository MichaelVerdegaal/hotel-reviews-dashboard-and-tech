###
# This file will change frequently until all the modules have been written, for testing purposes
###

import dash
import dash_core_components as dcc
import dash_html_components as html

from data.dashboard import create_worldmap, update_worldmap_settings
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
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
app.title = 'Hotel reviews sentiment analysis'
app.run_server(debug=True)
