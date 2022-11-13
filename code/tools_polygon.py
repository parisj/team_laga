import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer
from shapely.geometry import Polygon, MultiPolygon


def plot_multipoly(multipoly):
    
    """
    Polts a Multipolygon 

    Parameters
    ----------
    multipoly : shapely.Multipolygon 
           Multipolygon containing polygons

    Returns
    -------
    fig: Figure Matplotlib
    ax: Axis Matplotlib
    """
    
    #Scale points into map 
    transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
    
    fig, ax = plt.subplots()
    for poly in multipoly:
        
        #Scale and shift polygono points
        tmp = poly.exterior.xy
        x, y = transformer.transform(tmp[1], tmp[0])
        ax.plot(x, y)
        
    return fig, ax
    
def plot_poly(poly):
    
    """
    Plots a Polygon

    Parameters
    ----------
    poly : shapely.polygon

    Returns
    -------
    fig: Figure Matplotlib
    ax: Axis Matplotlib
    
    """
    
    transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')

    tmp = poly.exterior.xy
    x, y = transformer.transform(tmp[1], tmp[0])
    fig, ax = plt.subplots()
    ax.plot(x, y)
    return fig, ax
    
    
def create_index_intersection(file_path, multipoly):
    
    """
    Creates an List with indexes of all polygons from file_path
    intersecting with the given multipoly

    Parameters
    ----------
    file_path : Path to cvs of Coordinates
    multipoly : shapely.geometrie Multipolygon

    Returns
    -------
    Indexes (in file_path) of streets intersected by multipoly
    
    """
    
    #Prepare Points
    df_area = pd.read_csv(str(file_path), sep=";")
    js_area_s = json.loads(df_area['Geo Shape'][0])
    # area_np = np.array(js_area_s['coordinates'][0])
    
    # Create empty list
    list_index=[]
    
    # Enumerate and iterate over all Streets 
    for i, zone in enumerate(df_area['Geo Shape']):
        #print (zone, 'ZONE')
        js_points = json.loads(zone)
        points = np.array(js_points['coordinates'][0])
        
        # fix Dataset errors 
        if points.ndim == 3:
            points = points[0]
            
        # Create Polygon from current Iteration of streets
        poly_area_new = Polygon(tuple(points))
        if multipoly.intersects(poly_area_new):
            list_index.append(i)

    return list_index


def create_multipolygon(file, area=True):
    
    """
    Creates shapely.geometry Multipolygon

    Parameters
    ----------
    file :  Path to csv file from OSM
    area : Bool if area is wanted (unified) or seperate polygons

    Returns
    -------
    poly_area: shapely.geometrie Multipolynom
    
    """
    
    # create df from file path
    df_area = pd.read_csv(str(file), sep=";")
    
    # create first Polygon
    js_area_s = json.loads(df_area['Geo Shape'][0])
    area_np = np.array(js_area_s['coordinates'][0])
    poly_area = Polygon (area_np)
    
    if not area:
        list_noarea=[]
    # iterate over all point groups in Geo Shape (from OSM)
    for i, zone in enumerate( df_area['Geo Shape']):
        
        #creat json of all coordinates in the zone
        js_points = json.loads(zone)
        
        points = np.array(js_points['coordinates'][0])
        
        # fix dataset error
        if points.ndim == 3:
            points = points[0]

        # Creat Polygon with all point in the zone 
        poly_area_new = Polygon(tuple(points))
        
        # Add Polygon to the Multipolygon
        if area:
            poly_area=poly_area.union(poly_area_new)
        
        else:
            list_noarea.append(poly_area_new)
        
    if not area:
        poly_area=MultiPolygon(list_noarea)
    return poly_area

def import_intersection(data_street, *args):
    
    """
    import file path of streets 
    import file path of all areas wanted for intersection
    return index of all streets intersected by the area
    
    Parameters
    ----------
    data_street : path to csv file from OSM
    
     *args: paths to csv files from OSM describing
            the Areas for intersection

    Returns
    -------
    list of Indexes in data_street file ['Geo Shape']
    
    """
    
    # Create first area from args[0]
    poly_area = create_multipolygon(args[0])
    for arg in args:
        
        # no dublicate
        if arg != args[0]:
            
            # merge area from all args to first area
            poly_area = poly_area.union(create_multipolygon(arg))
        
    # retrieve indexes from intersection of streets with all areas
    indexs_street = create_index_intersection(data_street, poly_area)

    
    return indexs_street

def create_poly_with_indices(indices, file):
      
    """
    import file path of streets based on indices
    and create Multipoly    
    Parameters
    ----------
     indices: indices of Geo Shapes

    
     file : path to csv file from OSM
    
    
    Returns
    -------
    poly_indices: shapely.geometrix Multipolynom
    
    """
    
    list_poly=[]
    
    #import file
    df_import = pd.read_csv(file, sep=";")
    
    #add polygons based on indices to list
    for i in indices: 
        js_import = json.loads(df_import['Geo Shape'][i])
        df_import.to_csv("code/test/data_geo_shape_test.csv")
        np_import = np.array(js_import['coordinates'][0])
        poly_area = Polygon (np_import)
        list_poly.append(poly_area)
    # Convert List to Multipolygon  
    poly_indices = MultiPolygon(list_poly)
    return poly_indices




if __name__ == "__main__": 
    path_data_30 = "data/tempo-30-zonen.csv"
    path_strassenplan = "data/gemeindestrassenplan.csv"
    path_begegnungszonen = "data/begegnungszonen.csv"
    intersection = import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    # print(intersection)
