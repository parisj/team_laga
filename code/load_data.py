from pyproj import Transformer
import json
import numpy as np
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
from matplotlib import cm
from shapely.geometry import Polygon
from centerline.geometry import Centerline

import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

plt.close("all")

transformer = Transformer.from_crs('EPSG:4326', 'EPSG:3857', accuracy=0.5)
zonen_30 = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
begegnungszonen = pd.read_csv("data/begegnungszonen.csv", sep=";")
gemeindestrassen = pd.read_csv("data/gemeindestrassenplan.csv", sep=";")

ungeeignet = 0
geeignet = 0

max_distance = []
# for i in range(0, gemeindestrassen.shape[0]):
for i in range(0, 50):
    # Load data
    js = json.loads(gemeindestrassen['Geo Shape'][i])
    tmp = np.array(js['coordinates'][0])

    # transform decimal degrees to epsg
    x, y = transformer.transform(tmp[:, 1], tmp[:, 0])
    data = np.array([xyz for xyz in zip(x, y)])

    # Generic polygon shape of data (has interiors and exteriors)
    polygon = Polygon(data)

    print(gemeindestrassen["strassenna"].loc[i])
    print(gemeindestrassen["strassenkl"].loc[i])
    print(gemeindestrassen["strassennr"].loc[i])

    centerline = Centerline(polygon)
    p = gpd.GeoDataFrame(centerline)
    p = p.set_geometry(0)

    widths = p.distance(polygon.exterior)*2
    print("width", widths.mean())
    print("length", centerline.length/2)


    centerline = centerline.length/2
    n_units = centerline/40
    ex_polygon = polygon.area
    req_polygon = centerline * 3.8 + n_units * 10 * 3.8
    ents_polygon = ex_polygon - req_polygon
    print("entsiegelung_area", ents_polygon)

    if ents_polygon < 0:
        ungeeignet += 1
        print("ungeeignet")

    else:
        geeignet += 1
        print("geeignet")

print(ungeeignet/geeignet*100)


    #ex_polygon = (centerline.length/2) * (max_distance[-1] * 2)
    # try:
    #     centerline = Centerline(polygon)
    #     p = gpd.GeoDataFrame(centerline)
    #     p = p.set_geometry(0)

    #     max_distance.append(p.distance(polygon.exterior).max())
    #     print(max_distance[-1])
    #     print(centerline.length/2)

    #     breakpoint()

    #     ex_polygon = (centerline.length/2) * (max_distance * 2)
    #     req_polygon = centerline.length * 3.8
    #     rest_polygon = ex_polygon.area - req_polygon.area
    #     print(rest_polygon)

    #     breakpoint()
    # except:
    #     print("Error 420")


# breakpoint()

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

    # Convert (lat,lon) to (x,y,z). (Formula could potentially be improved)
    # x = r * np.sin(np.radians(tmp[:, 0])) * np.cos(np.radians(tmp[:, 1]))
    # y = r * np.sin(np.radians(tmp[:, 0])) * np.sin(np.radians(tmp[:, 1]))
    # z = r * np.cos(np.radians(tmp[:, 0]))
    # data = np.array([xyz for xyz in zip(x, y, z)])

    # fig, ax = plt.subplots()
    # ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
    # fig.savefig("/tmp/test.png")

    # Average radius of earth [m] (±10km)
# r = 6371000

# if __name__ == '__main__':
#     print("Ich ha en grosse")
