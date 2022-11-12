import tools_polygon as tp
import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import geopandas as gpd


path_data_30 = "code/data/tempo-30-zonen.csv"
path_strassenplan = "code/data/gemeindestrassenplan.csv"
path_begegnungszonen = "code/data/begegnungszonen.csv"
intersection = tp.import_intersection(path_strassenplan, path_begegnungszonen)

G_i=tp.create_poly_with_indices(intersection, path_strassenplan)
#G_i = tp.create_multipolygon(path_begegnungszonen)
#print(type(G_i))
#G=gpd.GeoDataFrame(G_i)



G = ox.graph_from_place('St. Gallen, Switzerland', simplify=True, network_type='drive_service')
fig, ax = ox.plot_graph(G, node_size=0, show=False)

breakpoint()
for poly in G_i: 
    #Scale and shif polygono points
    #tmp = poly.exterior.xy
    #x, y = transformer.transform(tmp[1], tmp[0])
    x, y = poly.exterior.xy
    ax.plot(x, y, c='#008f11')
plt.show()