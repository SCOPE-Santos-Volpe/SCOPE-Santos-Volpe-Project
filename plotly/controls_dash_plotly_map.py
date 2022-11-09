"""
This example is based on: https://stackoverflow.com/questions/71375339/plotly-mapbox-get-the-geometry-of-current-view-zoom-level
"""

import pandas as pd
import requests
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash
from dash.dependencies import Input, Output, State
import json
import numpy as np
import plotly.express as px
import geopandas as gpd
import shapely.geometry
from dash import Dash, dcc, html
import dash_table


fars_df = pd.read_csv("../FARS2020NationalCSV/accident.CSV", encoding_errors='ignore')
# fars_df = fars_df[['LATITUDE','LONGITUD','CITYNAME','COUNTYNAME','STATENAME']]
fars_df = fars_df.rename(columns={'LATITUDE': 'lat','LONGITUD': 'lon'})

print(fars_df.columns)
# print(fars_df[fars_df["LATITUDENAME"] == "Reported as Unknown"][["lat", "STATENAME", "COUNTYNAME", "CITYNAME"]])
# print(fars_df[fars_df["LONGITUDNAME"] == "Reported as Unknown"][["lon", "STATENAME", "COUNTYNAME", "CITYNAME"]])
fars_df = fars_df[fars_df["LATITUDENAME"] != "Reported as Unknown"]
fars_df = fars_df[fars_df["LONGITUDNAME"] != "Reported as Unknown"]


# some ways to specify the api token:
# token = open(".mapbox_token").read() # via file
# api_token = input("") # via pasting it into the command line input
api_token = "pk.eyJ1IjoibGlsb2hlaW5yaWNoIiwiYSI6ImNsOGR3ZmtzdjFldTMzb214cGY3OGtvcjgifQ.iJSaWES9W4WM2r8tOIOIoA" # via hardcoding

# MAPBOX STYLE OPTIONS:
# 'open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor'
# 'basic', 'streets', 'outdoors', 'light', 'dark', 'satellite', 'satellite- streets'


# # this creates a scattermapbox directly rather than as a layer, so it always plots. this isn't what we want i think.
# # https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
# fig = px.scatter_mapbox(fars_df,
#                 lat="lat", lon="lon",
#                 labels="FARS 2020 crashes",
#                 zoom=3,
#                 height = 600, width = 900,
#                 title='FARS 2020 Crashes',
#                 mapbox_style='basic',
#                 # color="lat",
#                 # text="lat",
#                 # size="lat",
#                 hover_name="CITYNAME",
#                 hover_data=["COUNTYNAME", "STATENAME"],
#                 color_discrete_sequence=["fuchsia"],
#                 opacity=0.0,
#                 )


# creates an empty scattermapbox, so it doesn't plot anything to start
#fig = go.Figure(go.Scattermapbox())
quakes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
fig = go.Figure(go.Densitymapbox(lat=quakes.Latitude, lon=quakes.Longitude, z=quakes.Magnitude, radius=10))
# fig = go.Figure(go.Densitymapbox(lat=fars_df["lat"], lon=fars_df["lon"], z=fars_df["PERSONS"], radius=20))

# sets attributes of the plot
fig.update_layout(
    # hovermode='closest', # not sure what this does
    mapbox_accesstoken=api_token,
    height = 500, width = 1000, # set the window size
    title='FARS 2020 Crashes', # title of window
    title_font_size = 18,
    font_size=16,
    mapbox_style="open-street-map", # set the map style. basic, light, dark, etc.
    mapbox=dict(
        accesstoken=api_token,
        bearing=0,
        center=go.layout.mapbox.Center(lat=40,lon=-95), # center the map on the middle of the US
        pitch=0,
        zoom=3 # zoom out to see the whole US
    )
)


#fig = go.Figure(go.Scattermapbox(mode = "markers+lines",lon = [10, 20, 30],lat = [10, 20,30],marker = {'size': 10}))
#fig.add_trace(go.Scattermapbox(mode = "markers+lines",lon = [-80, -95, -110], lat = [40, 30,50],marker = {'size': 10}))
fig.add_trace(go.Scattermapbox(mode = "lines",lon = [-96.5,-91,-91,-97.5,-96.5], lat = [43.5,43.5,48,49,43.5],marker = {'size': 10}))


# creates layers to plot
fig.update_layout(
    mapbox_layers=[
        {
            # "below": "traces",
            "circle": {"radius": 3},
            #"type" : "line",
            #"opacity": 1.0,
            "opacity": 0.5,
            #"line": {"width": 6},
            #"type" : "symbol",
            #"symbol": {"icon": "bar", "iconsize" : 10, "text" : "Hi"},
            "color":"rgb(0,0,255)",
            "minzoom": 4, # the minimum zoom to plot at
            "maxzoom": 6, # the maximum zoom to plot at
            "source": gpd.GeoSeries(
                fars_df.loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "fars1",

        },
        {
            "circle": {"radius": 6},
            "color":"rgb(0,0,255)",
            "minzoom": 6,
            "maxzoom": 9,
            "source": gpd.GeoSeries(
                fars_df.loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "fars2",
            "opacity": 0.6,
        },
        {
            "circle": {"radius": 9},
            "color":"rgb(0,0,255)",
            "minzoom": 9,
            "maxzoom": 14,
            "source": gpd.GeoSeries(
                fars_df.loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "fars3",
            "opacity": 0.7,
        },
        {
            "circle": {"radius": 12},
            "color":"rgb(0,0,200)",
            "minzoom": 14,
            # "maxzoom": 8,
            "source": gpd.GeoSeries(
                fars_df.loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "fars4",
            "opacity": 0.8,
        },
        # { # try adding datapoints for 10,000 points only to show how layers and colors can be used
        #     "circle": {"radius": 3},
        #     "color":"rgb(50,50,50)",
        #     "minzoom": 4,
        #     "maxzoom": 8,
        #     "source": gpd.GeoSeries(
        #         fars_df[:10000].loc[:, ["lon", "lat"]].apply(
        #             shapely.geometry.Point, axis=1)
        #     ).__geo_interface__,
        #     "name": "fars10k",
        #     "opacity": 0.3,
        # },
    ],
)




fig.update_layout(font_size=16, title={'xanchor': 'center','yanchor': 'top', 'y':1.0, 'x':0.5,}, title_font_size = 18, mapbox_accesstoken=api_token, legend = dict(itemsizing = 'constant'), margin = dict(t=20, b=0, l=0, r=0))



# fig.update_traces(text='lat', hovertextsrc="CITYNAME", # hoverinfo hoverlabel hoversrc hovertext hovertemplate hovertemplatesrc hovertextsrc hoverinfosrc
#                     # hover_data=["COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"],
#                     )

# this could fit by screen margin rather than size:
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



# DASH CODE
# Build App
app = JupyterDash(__name__)

app.layout = html.Div(
            className="content",
            children=[
		html.Div(
		    className="left_menu",
		    children=[
			html.Div(
			    'This is the left menu'
			),
		    ]
		),
		html.Div(
		    className="right_content",
		    children=[
			html.Div(
			    className="top_metrics",
			    children=[
			    'This is top metrics'
			    ]
			),
			html.Div(
			    'This down top metrics'
			),
		    ]
		),
		]
		)


app.layout = dash.html.Div([
    dash.html.H1('Hello'),
    dash.html.Div([dash.html.Div('Div', style={'color': 'blue', 'fontSize': 14}), dash.html.P('Example P', className='my-class', id='my-p-element')], style={'marginBottom': 50, 'marginTop': 25}),

    	dash.html.P('Hello2'),
    	dash.html.Div([
        	dcc.Checklist(['New York City', 'Montréal', 'San Francisco'], ['Montréal', 'San Francisco']),
        	dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
        ]),
        dash.dcc.Graph(id="mapbox_fig", figure=fig),
        dash.dcc.Store(
            id="points-store",
            data={
                "lat": [],
                "lon": [],
            },
        )
    ])


app.layout = html.Div([
    # first row
    html.Div(children=[
        # first column of first row
        html.Div(children=[
            html.P(id='text-2',
                   children='Radio boxes'),
            dcc.RadioItems(id = 'radio_item',
                           options = [dict(label = 'option A', value = 'A'),
                                      dict(label = 'option B', value = 'B'),
                                      dict(label = 'option C', value = 'C')],
                            value = 'A',
                            labelStyle={'display': 'block'}),

            html.P(id = 'text-1',
                   children = 'Checklist boxes'),

           dcc.Checklist(id = 'checklist_item',
               options = [dict(label = 'New York City', value = '1'),
                          dict(label = 'Montréal', value = '2'),
                          dict(label = 'San Francisco', value = '3')],
		  value = ['2', '3'],
		  labelStyle={'display': 'block'}),

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

        # second column of first row
        #html.Div(children=[
        #    dcc.Checklist(id = 'checklist-item-2',
        #               options = [dict(label = 'New York City', value = '1'),
        #                          dict(label = 'Montréal', value = '2'),
        #                          dict(label = 'San Francisco', value = '3')],
	#			  value = ['2', '3'],
	#		  labelStyle={'display': 'block'}),
	#
        #    html.P(id='text-2',
        #           children='Second paragraph'),
	#
        #], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

        # third column of first row
        html.Div(children=[
            #html.Div(dcc.Graph(id = 'main-graph',
            #                   figure = figure)),

            dash.dcc.Graph(id="mapbox_fig", figure=fig),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),
    ], className='row'),

    # second row
    html.Div(children=[
        html.Div(dash_table.DataTable(id = 'main-table',
                                      columns = [{"name": i, "id": i} for i in fars_df.columns],
                                      data = fars_df.to_dict('records'),
                                      style_table={'margin-left': '3vw', 'margin-top': '3vw'})),
    ], className='row'),
])


@app.callback(
    Output("points-store", "data"),
    # Output("debug_container", "children"), # can turn this back on to have checkbox to show window lat/lon info onscreen
    Input("mapbox_fig", "relayoutData"),
    Input("radio_item", "radio_item"),
    Input("checklist_item", "checklist_item"),
    # Input("refresh","value") # can turn this back on to have checkbox to show window lat/lon info onscreen
)

def mapbox_cb(mapbox_cfg, radio_item, checklist_item): #, refresh): # can turn this back on to have checkbox to show window lat/lon info onscreen
    # can turn this back on to have checkbox to show window lat/lon info onscreen
    # try:
    #     refresh = refresh[0]=="yes"
    # except Exception:
    #     refresh = False

    print("outputs", mapbox_cfg, radio_item, checklist_item)

    if mapbox_cfg and "mapbox.zoom" in mapbox_cfg.keys(): # and refresh:  # can turn this back on to have checkbox to show window lat/lon info onscreen
        bbox = np.array(mapbox_cfg["mapbox._derived"]["coordinates"])
        # bbox = bbox * .8
        data = {
            "lon": bbox[:, 0].tolist() + [mapbox_cfg["mapbox.center"]["lon"]],
            "lat": bbox[:, 1].tolist() + [mapbox_cfg["mapbox.center"]["lat"]],
        }

        # print out window center and bounds lat. & long. values in terminal as they update
        print("data[\"lon\"]", data["lon"])
        print("data[\"lat\"]", data["lat"])

        # can turn this back on to have checkbox to show window lat/lon info onscreen
        # return data, [
        #     dash.html.Pre(json.dumps(mapbox_cfg, indent=2)),
        #     dash.html.Pre(json.dumps(data, indent=2)),
        # ]
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
