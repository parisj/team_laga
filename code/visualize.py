import tools_polygon as tp
import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd


path_data_30 = "data/tempo-30-zonen.csv"
path_strassenplan = "data/gemeindestrassenplan.csv"
path_begegnungszonen = "data/begegnungszonen.csv"

intersection = tp.import_intersection(path_strassenplan, path_begegnungszonen)

G_i=tp.create_poly_with_indices(intersection, path_strassenplan)
print(type(G_i))
G=gpd.GeoDataFrame(G_i)

# create network from that bounding box
#G1 = ox.graph_from_place('St. Gallen, Switzerland', simplify=False, network_type='drive_service')

fig, ax = ox.graph_from_polygon(G_i)

plt.show()