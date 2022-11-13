import tools_polygon as tp
import osmnx as ox
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch

def ax_patch(ax, polygon, fc, ec, **kwargs):
    
    """
   Takes polygon or Multipolygon and existing axis, plots 
   polygons onto given axix
   Polygon ploted with Face Color and Edge Color 
    ----------
     ax: Matplotlib axis
     polygon: shapely.geometrie Polygon or Multipolygon
     fc: Color Value
     ec: Color Value
     **kwargs: keywords for add.patch

    
    Returns
    -------
    n no return 
    """
    
    # Check if Multipolygon
    if polygon.geom_type == 'MultiPolygon':
        
        #add individual polygon to patch
        for poly in polygon:
            patch = PolygonPatch(poly, fc=fc, ec=ec, **kwargs)
            ax.add_patch(patch)
    else:
        #add polygon to patch 
        patch = PolygonPatch(polygon, fc=fc, ec=ec, **kwargs)
        ax.add_patch(patch)

    return 0


def strd_osmnx_plot(Location, **kwargs):
    
    """
    import file path of streets based on indices
    and create Multipoly    
    Parameters for osmnx.graph_from_place function
    ----------
    Location: List in form ('Town, Country')
     **kwargs: for osmnx.graph_from_place
    
    
    Returns
    -------
    ax: axis of plot
    fig: figure of plot
    """
    
    G = ox.graph_from_place(Location, simplify=True, **kwargs)
    fig, ax = ox.plot_graph(G, node_size=0, show=False, edge_linewidth=0.1, edge_color='#C0C0C0', edge_alpha=0.5)
    
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
    
    G = ox.graph_from_point(coordinate, dist=distance, **kwargs)
    fig, ax = ox.plot_graph(G, node_size=0, show=False)
    
    
    return fig, ax
if __name__ == "__main__": 
    
    #fig, ax = point_osmnx_plot((9.5,48.91),400)
    #plt.show()
    
    path_data_30 = "code/data/tempo-30-zonen.csv"
    path_strassenplan = "code/data/gemeindestrassenplan.csv"
    path_begegnungszonen = "code/data/begegnungszonen.csv"
    
    area = tp.create_multipolygon(path_data_30)
    #intersection = tp.import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    
    # Plot 30 Zonen
    # fig, ax = strd_osmnx_plot("St. Gallen, Switzerland")
    # ax_patch(ax, area, fc='#98FB98', ec='#98FB98', alpha=0.4)
    # fig.savefig('plots/30_Zone_Plot.pdf', transparent=True)
    # plt.show()
    