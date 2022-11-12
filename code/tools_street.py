import tools_polygon as tp
import json
import numpy as np
import pandas as pd

from shapely.ops import nearest_points
from shapely.geometry import Point
from shapely.geometry import Polygon
from centerline.geometry import Centerline

import geopandas as gpd
import osmnx as ox

import warnings
from shapely.errors import ShapelyDeprecationWarning

from pyproj import Transformer

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('GTK4Cairo')
# ox.settings.default_crs = "epsg:3857"
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
transform_back = Transformer.from_crs('epsg:3857', 'epsg:4326')

def get_indices(start, end, length):
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


def insert_entsieglung(n_units, polygon, centerline):
    points = np.array(polygon.exterior.coords)
    n = 0
    entsieglungs_patches = []
    counter = 0
    while n <= n_units:
        random_index = np.random.randint(0, len(points) - 1)
        final_index = random_index + 1
        distance = 0
        while distance < 30:
            distance += np.linalg.norm(points[final_index] - points[final_index - 1])
            final_index += 1
            if final_index == len(points):
                final_index = 0 
        # TODO: Improve this
        if distance < 35:
            point_start = Point(points[random_index])
            point_end = Point(points[final_index])
            centerline_point_start = np.array(nearest_points(point_start, centerline)[1])
            centerline_point_end = np.array(nearest_points(point_end, centerline)[1])
            ps = [point_start, point_end, centerline_point_end, centerline_point_start]
            pol = Polygon(ps)
            entsieglungs_patches.append(pol)
            n += 1
            # if len(entsieglungs_patches) > 0:
            #     valid = True
            #     print()
            #     for patch in entsieglungs_patches:
            #         print(n, pol.distance(patch))
            #         if pol.distance(patch) == 0:
            #             valid = False
            #     if valid:
            #         entsieglungs_patches.append(pol)
            #         n += 1
            # else:
            #     entsieglungs_patches.append(pol)
        # counter += 1
        # if counter > 10000:
        #     entsieglungs_patches = []
        #     n = 0
        #     counter = 0
    return entsieglungs_patches


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
            print(i, "/", len(index_street))
            # Load data
            js = json.loads(df_street['Geo Shape'][i])
            tmp = np.array(js['coordinates'][0])

            x, y = transformer.transform(tmp[:, 1], tmp[:, 0])
            data = np.array([xyz for xyz in zip(x, y)])

            # Generic polygon shape of data (has interiors and exteriors)
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
                entsieglungs_patches = insert_entsieglung(n_units, polygon, centerline)

                current_coord = []
                for i in df_street['Geo Point'][i].split(','):
                    current_coord.append(float(i))

                G = ox.graph_from_point(current_coord, dist=100, network_type='all')
                fig, ax = ox.plot_graph(G, show=False)
                ax.plot(polygon.exterior.xy[0], polygon.exterior.xy[1])

                plt.show()

                breakpoint()

                fig, ax = plt.subplots()
                ax.plot(polygon.exterior.xy[0], polygon.exterior.xy[1])
                for line in centerline:
                    ax.plot(line.xy[0], line.xy[1], c='k')
                for ent_patch in entsieglungs_patches:
                    ax.plot(ent_patch.exterior.xy[0], ent_patch.exterior.xy[1], c='g')
                plt.show()

    return list_index


if __name__ == "__main__":
    path_data_30 = "data/tempo-30-zonen.csv"
    path_strassenplan = "data/gemeindestrassenplan.csv"
    path_begegnungszonen = "data/begegnungszonen.csv"
    index_intersection = tp.import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    index_width = import_width(path_strassenplan, index_intersection)
    
    print(index_intersection)
    print(index_width)
    breakpoint()
