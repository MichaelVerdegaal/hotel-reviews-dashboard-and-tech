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
