""" 
This example is based on: https://stackoverflow.com/questions/71375339/plotly-mapbox-get-the-geometry-of-current-view-zoom-level
"""

import pandas as pd
# import geopandas as gpd
import requests
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash
from dash.dependencies import Input, Output, State
import json
import numpy as np
import plotly.express as px

fars_df = pd.read_csv("FARS2020NationalCSV/accident.CSV", encoding_errors='ignore')
fars_df = fars_df[['LATITUDE','LONGITUD']]
fars_df = fars_df.rename(columns={'LATITUDE': 'lat','LONGITUD': 'lon'})

data = {'lat': [0],
        'lon': [0]}

# api_token = input("")
api_token = "pk.eyJ1IjoibGlsb2hlaW5yaWNoIiwiYSI6ImNsOGR3ZmtzdjFldTMzb214cGY3OGtvcjgifQ.iJSaWES9W4WM2r8tOIOIoA"

# fars_df
# # https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
fig = px.scatter_mapbox(fars_df, lat="lat", lon="lon", labels="FARS 2020 crashes", zoom=3,
                height = 800, width = 1200,
                title='FARS 2020 Crashes',
                mapbox_style='basic' 
                # 'open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen- terrain', 'stamen-toner', 'stamen-watercolor'
                # 'basic', 'streets', 'outdoors', 'light', 'dark', 'satellite', 'satellite- streets'
                # "mapbox://styles/strym/ckhd00st61aum19noz9h8y8kw"
                )
fig.update_layout(font_size=16,  title={'xanchor': 'center','yanchor': 'top', 'y':0.9, 'x':0.5,}, 
                title_font_size = 24, mapbox_accesstoken=api_token)


# Build App
app = JupyterDash(__name__)
app.layout = dash.html.Div(
    [
        dash.dcc.Checklist(
            options=[{"label":"refesh", "value":"yes"}],
            id="refresh",
        ),
        dash.dcc.Graph(id="mapbox_fig", figure=fig),
        dash.html.Div(
            id="debug_container",
        ),
        dash.dcc.Store(
            id="points-store",
            data={
                "lat": [],
                "lon": [],
            },
        ),
    ]
)


@app.callback(
    Output("points-store", "data"),
    Output("debug_container", "children"),
    Input("mapbox_fig", "relayoutData"),
    Input("refresh","value")
)
def mapbox_cb(mapbox_cfg, refresh):
    try:
        refresh = refresh[0]=="yes"
    except Exception:
        refresh = False
    if mapbox_cfg and "mapbox.zoom" in mapbox_cfg.keys() and refresh:
        bbox = np.array(mapbox_cfg["mapbox._derived"]["coordinates"])
        # bbox = bbox * .8
        data = {
            "lon": bbox[:, 0].tolist() + [mapbox_cfg["mapbox.center"]["lon"]],
            "lat": bbox[:, 1].tolist() + [mapbox_cfg["mapbox.center"]["lat"]],
        }

        return data, [
            dash.html.Pre(json.dumps(mapbox_cfg, indent=2)),
            dash.html.Pre(json.dumps(data, indent=2)),
        ]
    else:
        raise dash.exceptions.PreventUpdate


app.clientside_callback(
    """
    function(data, fig) {
        fig.data[1]['lat'] = data['lat'];
        fig.data[1]['lon'] = data['lon'];
        fig.layout.datarevision = fig.layout.datarevision + 1;
        /* return fig; */
        return JSON.parse(JSON.stringify(fig)); 
    }
    """,
    Output("mapbox_fig", "figure"),
    Input("points-store", "data"),
    State("mapbox_fig", "figure"),
)

app.run_server(mode="inline")
