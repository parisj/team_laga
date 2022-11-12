import tools_polygon
import json
import numpy as np
import pandas as pd

from shapely.geometry import Polygon
from centerline.geometry import Centerline
import geopandas as gpd

import warnings
from shapely.errors import ShapelyDeprecationWarning

from pyproj import Transformer

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')


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

    return list_index


if __name__ == "__main__": 
    path_data_30 = "data/tempo-30-zonen.csv"
    path_strassenplan = "data/gemeindestrassenplan.csv"
    path_begegnungszonen = "data/begegnungszonen.csv"
    index_intersection = tools_polygon.import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    index_width = import_width(path_strassenplan, index_intersection)
    print(index_intersection)
    print(index_width)
    breakpoint()
