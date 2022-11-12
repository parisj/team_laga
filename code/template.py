import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
def import_intersection(data_street, *args):

    # df_area = pd.read_csv(args[0], sep=";")
    # js_area = json.loads(df_area['Geo Shape'][0])
    
    # df = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
    # js = json.loads(df['Geo Shape'][0])
    # data = np.array(js['coordinates'][0])
    
    df_street = pd.read_csv(data_street, sep=";")
    #print(tuple(df_street))
    js_street = json.load(df_street['Geo Shape'][0])
    print(df_street)
    street =np.array(js_street['coordinates'][0])
    print(street)
    for arg in args:
        
        df_next_area = pd.read_csv(arg, sep=";")
        js_next_area = json.loads(df_next_area['Geo Shape'][0])
        next_area = np.array(js_next_area['coordinates'][0])

        area = area.append(next_area)
        
    polygon_area = Polygon(tuple(area))
    polygon_street= Polygon(tuple(street))
    intersection = polygon_area.intersect(polygon_street)
    #print(intersection)
    
    print(data)
    print(data[0])
    
    fig, ax = plt.subplots()
    ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
    plt.show()

    intersetion = 0
    return intersection



if __name__ == "__main__": 
    path_data_30 = "data/tempo-30-zonen.csv"
    path_strassenplan = "data/gemeindestrassenplan.csv"
    path_begegnungszonen = "data/tempo-30-zonen.csv"
    intersection = import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    
    