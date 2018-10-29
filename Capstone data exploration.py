
# coding: utf-8

# # DATA EXPLORATION FOR CAPSTONE

# ## A. Import supporting packages

# In[2]:


import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import json

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim

import requests
from pandas.io.json import json_normalize

import matplotlib.cm as cm
import matplotlib.colors as colors

from sklearn.cluster import KMeans

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # map rendering library

import altair as alt
import requests
import pandas as pd

import json
import csv

print('Libraries imported.')


# ## B. Load data

# a. CSV with cleaned data from foursquare API and Zillow median home prices by SF neighborhood

# In[3]:


sf_data = pd.read_csv('/resources/TDI1/SF_NEIGHBORHOOD_FEATURES.csv', dtype=object, index_col=0)


# In[15]:


sf_data.head(1)


# In[16]:


sf_data.median_price = sf_data.median_price.astype(float)
sf_data.latitude = sf_data.latitude.astype(float)
sf_data.longitude = sf_data.longitude.astype(float)
sf_data['Cluster Labels'] = sf_data['Cluster Labels'].astype(int)


# ## C. Map of median housing prices by neighborhood

# In[13]:


latitude = 37.77
longitude = -122.42
sfmap = folium.Map(location=[latitude, longitude], zoom_start=12)
sfmap.choropleth(
    geo_data = '/resources/TDI1/Planning Neighborhood Groups Map.geojson',
    data = sf_data,
    columns=['neighborhood', 'median_price'],
    key_on = 'feature.properties.neighborho',
    fill_color='YlOrRd', 
    fill_opacity=0.75, 
    line_opacity=0.2,
    legend_name='Housing prices in SF'
)
sfmap


# ## D. Map of neighborhood clusters

# Using k-means clustering on neighborhood business features

# In[20]:


kclusters = 8
latitude = 37.77
longitude = -122.42
# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=12)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(sf_data['latitude'], sf_data['longitude'], sf_data['neighborhood'], sf_data['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=15,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.8).add_to(map_clusters)
       
map_clusters

