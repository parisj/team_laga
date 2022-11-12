import tools_polygon as tp
import matplotlib.pyplot as plt

from pyproj import Transformer

# plt.style.use('dark_background')
transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')

def plot_multipoly(multipoly, c='w'):
    fig, ax = plt.subplots()
    for poly in multipoly:
        tmp = poly.exterior.xy
        x, y = transformer.transform(tmp[1], tmp[0])
        ax.plot(x, y, c=c, lw=0.1)
    ax.axis('off')
    # ax.xaxis.set_visible(False)
    # ax.yaxis.set_visible(False)
    return fig, ax

if __name__ == "__main__": 
    path_data_30 = "data/tempo-30-zonen.csv"
    path_strassenplan = "data/gemeindestrassenplan.csv"
    path_begegnungszonen = "data/begegnungszonen.csv"
    intersection = tp.import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)
    multi_p = tp.create_multipolygon(path_strassenplan, area=False)
    fig, ax = plot_multipoly(multi_p, '#008f11')
    fig.savefig("../plots/title_picture.pdf", transparent=True)
    # plt.show()
