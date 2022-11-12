import tools_polygon as tp
import osmnx as ox
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch
from shapely.geometry import Polygon, MultiPolygon

def ax_patch(ax, polygon, fc, ec):
    
    if polygon.geom_type == 'MultiPolygon':
        for poly in polygon:
            patch = PolygonPatch(poly, fc=fc, ec=ec)
            ax.add_patch(patch)
    else:
        patch = PolygonPatch(polygon, fc=fc, ec=ec)
        ax.add_patch(patch)

    return 0

def strd_osmnx_plot(town,city, **kwargs):
    
    G = ox.graph_from_place(town, city, simplify=True, network_type='drive_service')
    fig, ax = ox.plot_graph(G, node_size=0, show=False)
    
    return fig, ax

def point_osmnx_plot(coordinate, distance, **kwargs):
    
    G= ox.graph_from_point(coordinate, dist=distance, network_type='drive_service')
    fig, ax = ox.plot_graph(G, node_size=0, show=False)
    
    return fig, ax
if __name__ == "__main__": 
    
    # fig, ax = point_osmnx_plot((9.3,47.0), 400)
    # plt.show()
    
    
    strd_osmnx_plot("St. Gallen", "Switzerland")
    plt.show()
    