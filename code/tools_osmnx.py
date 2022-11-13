import tools_polygon as tp
import osmnx as ox
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, MultiPolygon

def ax_patch(ax, polygon, fc, ec):
    """
   Takes polygon or Multipolygon and existing axis, plots 
   polygons onto given axix
   Polygon ploted with Face Color and Edge Color 
    ----------
     ax: Matplotlib axis
     polygon: shapely.geometrie Polygon or Multipolygon
     fc: Color Value
     ec: Color Value
    
     file : path to csv file from OSM
    
    
    Returns
    -------
    n no return 
    """
    
    if polygon.geom_type == 'MultiPolygon':
        for poly in polygon:
            patch = PolygonPatch(poly, fc=fc, ec=ec)
            ax.add_patch(patch)
    else:
        patch = PolygonPatch(polygon, fc=fc, ec=ec)
        ax.add_patch(patch)

    return 0


def strd_osmnx_plot(town, country, **kwargs):
    """
    import file path of streets based on indices
    and create Multipoly    
    Parameters for osmnx.graph_from_place function
    ----------
     town: String, name of town
     country: String, name of country
    
     **kwargs: for osmnx.graph_from_place
    
    
    Returns
    -------
    ax: axis of plot
    fig: figure of plot
    """
    
    
    G = ox.graph_from_place(town, city, simplify=True, network_type='drive_service')
    fig, ax = ox.plot_graph(G, node_size=0, show=False)
    
    return fig, ax


def point_osmnx_plot(coordinate, distance, **kwargs):
    """
    return fig, ax from a osmnx plot with at wanted coordinantes
    with a distance, more options for 
    ----------
     indices: indices of Geo Shapes

    
     file : path to csv file from OSM
    
    
    Returns
    -------
    poly_indices: shapely.geometrix Multipolynom
    """
    
    G= ox.graph_from_point(coordinate, dist=distance, network_type='drive_service')
    fig, ax = ox.plot_graph(G, node_size=0, show=False)
    
    return fig, ax
if __name__ == "__main__": 
    
    # fig, ax = point_osmnx_plot((9.3,47.0), 400)
    # plt.show()
    
    
    strd_osmnx_plot("St. Gallen", "Switzerland")
    plt.show()
    