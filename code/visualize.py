import tools_polygon as tp
import osmnx as ox
import matplotlib.pyplot as plt
from descartes.patch import PolygonPatch


BLUE = '#6699cc'
GRAY = '#999999'

path_data_30 = "code/data/tempo-30-zonen.csv"
path_strassenplan = "code/data/gemeindestrassenplan.csv"
path_begegnungszonen = "code/data/begegnungszonen.csv"
intersection = tp.import_intersection(path_strassenplan, path_begegnungszonen)

G_i=tp.create_poly_with_indices(intersection, path_strassenplan)
#G_i = tp.create_multipolygon(path_begegnungszonen)
#print(type(G_i))
#G=gpd.GeoDataFrame(G_i)

#Inputs Polygon, Multipolygon

G = ox.graph_from_place('St. Gallen, Switzerland', simplify=True, network_type='drive_service')
fig, ax = ox.plot_graph(G, node_size=0, show=False)


for poly in G_i: 
    #Scale and shif polygono points
    #tmp = poly.exterior.xy
    #x, y = transformer.transform(tmp[1], tmp[0])
    patch = PolygonPatch(poly, fc=BLUE, ec=BLUE)
    ax.add_patch(patch)
    
plt.show()