import pandas as pd
# import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import shapely.geometry
import numpy as np
import plotly


fars_df = pd.read_csv("../FARS2020NationalCSV/accident.CSV", encoding_errors='ignore')
# print(fars_df[["LATITUDE", "STATENAME", "COUNTYNAME", "CITYNAME"]])
# pd.set_option('display.max_columns', 15)

print(fars_df.columns)
fars_df = fars_df[fars_df["LATITUDENAME"] != "Reported as Unknown"]
fars_df = fars_df[fars_df["LONGITUDNAME"] != "Reported as Unknown"]
# fars_df = fars_df[:993]
fars_df = fars_df.rename(columns={'LATITUDE': 'lat','LONGITUD': 'lon'})



scl = [
    [0.0, 'rgb(165,0,38)'],
    [1.0, 'rgb(49,54,149)']
]
data = [ go.Scattermapbox(
        lon = fars_df['lon'],
        lat = fars_df['lat'],
        mode = 'markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color =  fars_df['FUNC_SYS'],
            colorscale = scl,
        ),
        name = "all crashes",
        hovertext=fars_df[["COUNTYNAME", "STATENAME", "ROUTENAME", "TWAY_ID", "TWAY_ID2", "RUR_URBNAME", "FUNC_SYSNAME", "RD_OWNERNAME"]],
        hoverinfo='all',
        # minzoom=5,
        ),

        go.Scattermapbox(
        lon = fars_df[:10000]['lon'],
        lat = fars_df[:10000]['lat'],
        mode = 'markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color = 'red'
        ),
       name='first 10k crashes'),

        # go.Scattermapbox(
        # lon = fars_df[10000:20000]['lon'],
        # lat = fars_df[10000:20000]['lat'],
        # mode = 'markers',
        # marker=go.scattermapbox.Marker(
        # size=5,
        # color = 'grey'
        # ),
        # name = "target"
        # )
       ]


api_token = "pk.eyJ1IjoibGlsb2hlaW5yaWNoIiwiYSI6ImNsOGR3ZmtzdjFldTMzb214cGY3OGtvcjgifQ.iJSaWES9W4WM2r8tOIOIoA"

layout = go.Layout(
        autosize=True,
        # hovermode='closest',
    	height = 650, width = 1200, # set the window size
    	title='FARS 2020 Crashes', # title of window
        mapbox=go.layout.Mapbox(
            accesstoken=api_token,
            bearing=0,
            center=go.layout.mapbox.Center(lat=40,lon=-95),
            #go.layout.mapbox.Center(
            #    lat=np.mean(fars_df['lat']),
            #    lon=np.mean(fars_df['lon'])
        #),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)


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


fig.show()
