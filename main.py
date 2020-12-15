###
# This file will change frequently until all the modules have been written, for testing purposes
###

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go

from config import MBTOKEN
from data.database import *

# Data
db = create_connection()
df = query_hotels(db)

# Worldmap
fig = go.Figure(go.Scattermapbox(
    lat=df['lat'],
    lon=df['lng'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=14
    ),
    customdata=np.stack((df['Hotel_Name'], df['count']), axis=-1),
    hovertemplate='<extra></extra><em>%{customdata[0]}  </em><br>',
))

fig.update_layout(
    mapbox=dict(
        accesstoken=MBTOKEN,
        center=go.layout.mapbox.Center(lat=50, lon=0),
        zoom=3
    )
)

# Dash app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
app.title = 'Hotel reviews sentiment analysis'
app.run_server(debug=True)
