import json
import numpy as np
import pandas as pd

from shapely.ops import nearest_points
from shapely.geometry import Point
from shapely.geometry import Polygon
from centerline.geometry import Centerline
from descartes.patch import PolygonPatch

import geopandas as gpd
import osmnx as ox

import warnings
from shapely.errors import ShapelyDeprecationWarning

from pyproj import Transformer

import matplotlib
import matplotlib.pyplot as plt

import tools_polygon as tp
import tools_osmnx as to

matplotlib.use('GTK4Cairo')
# ox.settings.default_crs = "epsg:3857"
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
transformer_back = Transformer.from_crs('epsg:3857', 'epsg:4326')


def get_indices(start, end, length):
    """
    import start and end index of points
    import length of points array
    return list of indices between start and end

    Parameters
    ----------
    start : start index
    end : end index
    length : length of array

    Returns
    -------
    list of indices from start to end
    """
    indices = [start]
    completed = False
    it = start
    while completed == False:
        it += 1
        if it == length:
            it = 0
        indices.append(it)
        if it == end:
            completed = True
    return indices


def find_unsealing_patches(points, centerline, n_units=1, distance=30, d_thr=35):
    """
    import point and centerline geometries
    import desired number of patches
    import geometric constraints for patches
    return list of patches

    Parameters
    ----------
    points : list of points
    centerline : centerline shape
    n_units : number of patches
    distance : size of patches
    d_thr : distance threshold

    Returns
    -------
    list of patches
    """
    n = 0
    patch_list = []
    while n <= n_units:
        rand_i = np.random.randint(0, len(points) - 1)
        final_i = rand_i + 1
        distance = 0
        while d < distance:
            d += np.linalg.norm(points[final_i] - points[final_i - 1])
            final_i += 1
            if final_i == len(points):
                final_i = 0
        if d < d_thr:
            p1 = Point(points[rand_i])
            p2 = Point(points[final_i])
            p3 = np.array(nearest_points(p1, centerline)[1])
            p4 = np.array(nearest_points(p2, centerline)[1])
            patch_list.append(Polygon([p1, p2, p4, p3]))
            n += 1
    return patch_list


def import_width(data_street, index_street, width=7.6):
    """
    import file path of streets
    import indices of streets that should be considered
    return index of all streets that are less than width

    Parameters
    ----------
    data_street : path to csv file from OSM
    index_street :
    width : desired width of street

    Returns
    -------
    list of indices in data_street file
    """
    list_index = []
    A_potential = 0
    df_street = pd.read_csv(data_street, sep=";")

    for i in index_street:
        strassenkl = df_street["strassenkl"].loc[i]
        if "W" not in strassenkl:
            js = json.loads(df_street['Geo Shape'][i])
            tmp = np.array(js['coordinates'][0])

            x, y = transformer.transform(tmp[:, 1], tmp[:, 0])
            data = np.array([xyz for xyz in zip(x, y)])
            polygon = Polygon(data)

            # Centerline
            centerline = Centerline(polygon)
            p = gpd.GeoDataFrame(centerline)
            p = p.set_geometry(0)

            widths = p.distance(polygon.exterior)
            width_lower_end = 2 * (widths.mean() - widths.std())
            length = centerline.length / 2

            n_units = length / 40
            A_entsieglung = n_units * 30 * 3.8

            if width_lower_end >= width:
                list_index.append(i)
                A_potential += A_entsieglung
                
                # entsieglungs_patches = find_unsealing_patches(np.array(polygon.exterior.coords), centerline, n_units)

                # current_coord = []
                # for ind in df_street['Geo Point'][i].split(','):
                #     current_coord.append(float(ind))

                # # G = ox.graph_from_point(current_coord, dist=400, network_type='all')
                # # fig, ax = ox.plot_graph(G, show=False)
                # fig, ax = to.point_osmnx_plot(current_coord, 600)
                # # ax.plot(polygon_gps.exterior.xy[0], polygon_gps.exterior.xy[1])
                # # ax.plot(entsieglungs_patches[0].exterior.xy[0], entsieglungs_patches[0].exterior.xy[1], c="r")
                # to.ax_patch(ax, entsieglungs_patches[0])
                # # patch = PolygonPatch(entsieglungs_patches[0], fc="b", ec="b")
                # # ax.add_patch(patch)

                # plt.show()

                # breakpoint()

                # fig, ax = plt.subplots()
                # ax.plot(polygon.exterior.xy[0], polygon.exterior.xy[1], c='k', lw=0.1)
                # # for line in centerline:
                # #     ax.plot(line.xy[0], line.xy[1], c='k')
                # for ent_patch in entsieglungs_patches:
                #     ax.plot(ent_patch.exterior.xy[0], ent_patch.exterior.xy[1], c='g', lw=0.1)
                #     # patch = PolygonPatch(ent_patch, fc="g", ec="g")
                #     # ax.add_patch(patch)
                # ax.axis('off')
                # # fig.savefig("../plots/centerline_" + str(i) + ".pdf", transparent=True)
                # fig.savefig("../plots/entsieglungen_" + str(i) + ".pdf", transparent=True)
                # # plt.show()

    print(A_entsieglung)
    return list_index


if __name__ == "__main__":
    path_data_30 = "../data/tempo-30-zonen.csv"
    path_strassenplan = "../data/gemeindestrassenplan.csv"
    path_begegnungszonen = "../data/begegnungszonen.csv"
    index_intersection = tp.import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    index_width = import_width(path_strassenplan, index_intersection)
