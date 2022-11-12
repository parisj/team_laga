import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import cm

from shapely.geometry import Polygon

from centerline.geometry import Centerline
import geopandas as gpd

import warnings
from shapely.errors import ShapelyDeprecationWarning
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

plt.close("all")

from pyproj import Transformer
transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')

zonen_30 = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
begegnungszonen = pd.read_csv("data/begegnungszonen.csv", sep=";")
gemeindestrassen = pd.read_csv("data/gemeindestrassenplan.csv", sep=";")

# Average radius of earth [m] (±10km)
r = 6371000

widths_all = []
# for i in range(0, gemeindestrassen.shape[0]):
for i in range(0, 6):
    # Load data
    js = json.loads(gemeindestrassen['Geo Shape'][i])
    tmp = np.array(js['coordinates'][0])

    # Convert (lat,lon) to (x,y,z). (Formula could potentially be improved)
    # x = r * np.sin(np.radians(tmp[:, 0])) * np.cos(np.radians(tmp[:, 1]))
    # y = r * np.sin(np.radians(tmp[:, 0])) * np.sin(np.radians(tmp[:, 1]))
    # z = r * np.cos(np.radians(tmp[:, 0]))
    # data = np.array([xyz for xyz in zip(x, y, z)])

    x, y = transformer.transform(tmp[:,1], tmp[:,0])
    data = np.array([xyz for xyz in zip(x, y)])
    
    # Generic polygon shape of data (has interiors and exteriors)
    polygon = Polygon(data)

    # fig, ax = plt.subplots()
    # ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
    # fig.savefig("/tmp/test.png")

    print(gemeindestrassen["strassenna"].loc[i])
    print(gemeindestrassen["strassenkl"].loc[i])
    print(gemeindestrassen["strassennr"].loc[i])

    try:
        centerline = Centerline(polygon)
        p = gpd.GeoDataFrame(centerline)
        p = p.set_geometry(0)

        widths = p.distance(polygon.exterior)
        width_lower_end = 2 * (widths.mean() - widths.std())

        widths_all.append(width_lower_end)
        print(widths_all[-1])
        print(centerline.length/2)
    except:
        print("Error 420")
        
breakpoint()

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
