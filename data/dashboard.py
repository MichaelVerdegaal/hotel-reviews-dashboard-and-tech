import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from config import MBTOKEN


def create_worldmap(lat_list, long_list, customdata):
    """
    Creates an instance of a scatterplot map
    :param lat_list: collection of latitude coordinates
    :param long_list: collection of longitude coordinates
    :param customdata: extra information to be displayed on the hover label
    :return: plotly map figure
    """
    fig = go.Figure(go.Scattermapbox(
        lat=lat_list,
        lon=long_list,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        customdata=customdata,
        hovertemplate='<extra></extra><em>%{customdata[0]}</em><br>%{customdata[1]} reviews',
    ))
    return fig


def update_worldmap_settings(fig):
    """
    Set some settings of a plotly map figure that you can't/don't want to set at instantiation
    :param fig: plotly map figure
    """
    fig.update_layout(
        mapbox=dict(
            accesstoken=MBTOKEN,
            center=go.layout.mapbox.Center(lat=50, lon=0),
            zoom=3
        )
    )


def create_dash_app(fig):
    """
    Create dashboard app object
    :param fig: plotly map figure
    :return: dash app
    """
    app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
    app.layout = create_dash_layout(fig)
    app.title = 'Hotel reviews sentiment analysis'
    return app


def create_dash_layout(fig):
    """
    Create the dashboard layout for a dash app
    :param fig: plotly map figure
    :return: layout
    """
    layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    return layout
