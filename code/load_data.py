import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import cm

from shapely.geometry import Polygon
from shapely.geometry import LineString
from shapely.geometry.polygon import LinearRing

from centerline.geometry import Centerline
import geopandas as gpd

import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# import osmnx
# import osmnx as ox
# import geopandas as gpd

# Get place boundary related to the place name as a geodataframe
# area = ox.graph_from_address("Hochwachtstrasse, St. Gallen, Switzerland")
# ox.plot_graph(area, save=True, filepath="test.png", show=Falsew)

# breakpoint()

# from osmapi import OsmApi
# MyApi = OsmApi()

zonen_30 = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
begegnungszonen = pd.read_csv("data/begegnungszonen.csv", sep=";")
gemeindestrassen = pd.read_csv("data/gemeindestrassenplan.csv", sep=";")

r = 6371000

# breakpoint()

begegnungszonen_js = json.loads(gemeindestrassen['Geo Shape'][1])
data = np.array(begegnungszonen_js['coordinates'][0])

x = r * np.sin(np.radians(data[:, 0])) * np.cos(np.radians(data[:, 1]))
y = r * np.sin(np.radians(data[:, 0])) * np.sin(np.radians(data[:, 1]))
z = r * np.cos(np.radians(data[:, 0]))

data = np.array([xyz for xyz in zip(x, y, z)])
line = LinearRing(data)

# attributes = {"id": 1, "name": "polygon", "valid": True}

polygon = Polygon(data)
centerline = Centerline(polygon)
p = gpd.GeoDataFrame(centerline)
p = p.set_geometry(0)

print(p.distance(line).max())

max_distance = []
for i in range(0, gemeindestrassen.shape[0]):
    js = json.loads(gemeindestrassen['Geo Shape'][i])
    data = np.array(js['coordinates'][0])

    x = r * np.sin(np.radians(data[:, 0])) * np.cos(np.radians(data[:, 1]))
    y = r * np.sin(np.radians(data[:, 0])) * np.sin(np.radians(data[:, 1]))
    z = r * np.cos(np.radians(data[:, 0]))

    data = np.array([xyz for xyz in zip(x, y, z)])
    line = LinearRing(data)

    polygon = Polygon(data)
    print(i, data.shape)
    try:
        centerline = Centerline(polygon)
        p = gpd.GeoDataFrame(centerline)
        p = p.set_geometry(0)

        max_distance.append(p.distance(line).max())
    except:
        print(i)

breakpoint()

# breakpoint()
# breakpoint()
# print(line.area)

# # X, Y, Z = np.meshgrid(x, y, z)
# # breakpoint()
# box = line.minimum_rotated_rectangle
# # breakpoint()
# fig, ax = plt.subplots()
# ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
# ax.plot(data[-1, 0], data[-1, 1], ls="-", marker="o", color="r")
# x,y = centerline.geoms.exterior.xy
# ax.plot(x,y)
# # Plot the surface.
# # surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
# #                        linewidth=0, antialiased=False)
# fig.savefig("/tmp/test.png")

# breakpoint()
