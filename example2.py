import pandas as pd
# import plotly.graph_objects as go
# import numpy as np
import plotly.express as px
# 
import plotly.graph_objects as go
import geopandas as gpd
import shapely.geometry


fars_df = pd.read_csv("./FARS2020NationalCSV/accident.CSV", encoding_errors='ignore')
# print(fars_df[["LATITUDE", "STATENAME", "COUNTYNAME", "CITYNAME"]])
# pd.set_option('display.max_columns', 15)

print(fars_df.columns)
# print(fars_df[fars_df["LATITUDENAME"] == "Reported as Unknown"][["LATITUDE", "STATENAME", "COUNTYNAME", "CITYNAME"]])
# print(fars_df[fars_df["LONGITUDNAME"] == "Reported as Unknown"][["LONGITUD", "STATENAME", "COUNTYNAME", "CITYNAME"]])
fars_df = fars_df[fars_df["LATITUDENAME"] != "Reported as Unknown"]
fars_df = fars_df[fars_df["LONGITUDNAME"] != "Reported as Unknown"]
# fars_df = fars_df[:993]
fars_df = fars_df.rename(columns={'LATITUDE': 'lat','LONGITUD': 'lon'})

# fig = px.scatter_mapbox(fars_df, lat="LATITUDE", lon="LONGITUD", hover_name="CITYNAME", 
#                         hover_data=["COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"],
#                         # color_discrete_sequence=["blue"], 
#                         zoom=3, height=300)


fig = go.Figure(go.Scattermapbox())


# this creates a scattermapbox directly rather than as a layer, so it always plots. this isn't what we want i think.
# https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
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
#                 # color_discrete_sequence=["fuchsia"],
#                 opacity=0.0,
#                 )

# fig.update_layout(mapbox_style="open-street-map")
api_token = "pk.eyJ1IjoibGlsb2hlaW5yaWNoIiwiYSI6ImNsOGR3ZmtzdjFldTMzb214cGY3OGtvcjgifQ.iJSaWES9W4WM2r8tOIOIoA"
# fig.update_layout(mapbox_style="dark", mapbox_accesstoken=api_token)

fig.update_layout(
    # hovermode='closest', # not sure what this does
    height = 650, width = 1200, # set the window size
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

# adds the title 
fig.update_layout(font_size=16, title={'xanchor': 'center','yanchor': 'top', 'y':0.9, 'x':0.5,}, title_font_size = 18, mapbox_accesstoken=api_token)

# creates layers to plot
fig.update_layout(
    mapbox_layers=[
        {
            # "below": "traces",
            "circle": {"radius": 3},
            "color":"blue",
            "minzoom": 4, # the minimum zoom to plot at
            "maxzoom": 10, # the maximum zoom to plot at
            "source": gpd.GeoSeries(
                fars_df.loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "FARS 2020 Cccrashes",
            "opacity": 0.5,
        },
        {
            "circle": {"radius": 10},
            "color":"green",
            "minzoom": 10,
            # "maxzoom": 8,
            "source": gpd.GeoSeries(
                fars_df.loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "FARS 2020 Cccrashes",
            "opacity": 0.5,
        },
        { # try adding datapoints for 10,000 points only to show how layers and colors can be used
            "circle": {"radius": 3},
            "color":"red",
            "minzoom": 4,
            "source": gpd.GeoSeries(
                fars_df[:10000].loc[:, ["lon", "lat"]].apply(
                    shapely.geometry.Point, axis=1)
            ).__geo_interface__,
            "name": "FARS 2020 Cccrashes",
            "opacity": 1.0,
        },
    ],
)

fig.add_trace(go.Scattermapbox(
        lat=fars_df['lat'],
        lon=fars_df['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=1,
            color='rgb(0, 0, 255)',
            opacity=0.1
        ),
        text=fars_df[["CITYNAME", "COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"]],
        hoverinfo='all',
        name="all crashes",
    ))

fig.add_trace(go.Scattermapbox(
        lat=fars_df[:10000]['lat'],
        lon=fars_df[:10000]['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=1,
            color='rgb(255, 0, 0)',
            opacity=0.1
        ),
        text=["CITYNAME", "COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"],
        hoverinfo='all',
        name="first 10k crashes",
    ))


# fig.update_traces(text='lat', hovertextsrc="CITYNAME", hoverinfo="all", 
#     # hoverlabel="CITYNAME", 
#     # hoversrc="CITYNAME", 
#     hovertext="CITYNAME", hovertemplate="CITYNAME", hovertemplatesrc="CITYNAME", 
#     hoverinfosrc="CITYNAME",
#                     # hover_data=["COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"],
#                     )


# THIS ONE WORKED A BIT
fig.add_trace(px.scatter_mapbox(fars_df, 
                lat="lat", lon="lon", 
                labels="FARS 2020 crashes", 
                zoom=3,
                height = 600, width = 900,
                title='FARS 2020 Crashes',
                mapbox_style='basic',
                # color="lat",
                # text="lat",
                # size="lat",
                hover_name="CITYNAME", 
                hover_data=["COUNTYNAME", "STATENAME"], 
                # color_discrete_sequence=["fuchsia"],
                opacity=0.0,
                ).data[0])

# fig.add_trace(px.scatter_mapbox(fars_df[:10000], 
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
#                 # color_discrete_sequence=["fuchsia"],
#                 opacity=0.0,
#                 ).data[0], color="red")



# fig.add_trace(px.scatter_mapbox(fars_df, #name="FARS2020 trace",
#             opacity=0.5,
#             lon=fars_df["lat"],
#             lat=fars_df["lon"],
#              ))


# # https://plotly.com/python/reference/scattermapbox/
# trace=dict(type='scattermapbox',
#             name="FARS2020 trace",
#             showlegend=True,
#             opacity=0.5,
#             mode="markers",
#             lon=fars_df["lat"],
#             lat=fars_df["lon"],
#             hovertext=fars_df[["COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"]],
#             hoverinfo='all',
#             # mode='markers',
#             # hovertemplate 
#             # text=regions,
#             # marker=dict(size=[5]*11+[8]*11, color=['red']*11+['green']*11),
#             # hoverinfo='text'
#              )
# fig.add_trace(trace)


# # USGS Imagery map example
# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "sourceattribution": "United States Geological Survey",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         },
        # {
        #     "sourcetype": "raster",
        #     "sourceattribution": "Government of Canada",
        #     "source": ["https://geo.weather.gc.ca/geomet/?"
        #                "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
        #                "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
        # }
#       ])

#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()




# # Everywhere in this page that you see fig.show(), you can display the same figure in a Dash application by 
# # passing it to the figure argument of the Graph component from the built-in dash_core_components package like this:

# import plotly.graph_objects as go # or plotly.express as px
# fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# # fig.add_trace( ... )
# # fig.update_layout( ... )

# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

