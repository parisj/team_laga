import tools_osmnx as to
import tools_polygon as tp
import tools_street as ts
import matplotlib.pyplot as plt

def main():
    # Define paths
    path_data_30 = "../data/tempo-30-zonen.csv"
    path_strassenplan = "../data/gemeindestrassenplan.csv"
    path_begegnungszonen = "../data/begegnungszonen.csv"

    # Get streets, intersecting with 30-zone and begegnungszone
    intersection = tp.import_intersection(path_strassenplan, path_data_30, path_begegnungszonen)

    # Filter streets based on width
    index_width = ts.import_width(path_strassenplan, intersection)

    # Combine index list to multipolygon
    streets = tp.create_poly_with_indices(index_width, path_strassenplan)

    # Plot results
    fig, ax = to.strd_osmnx_plot("St. Gallen, Switzerland")
    to.ax_patch(ax, streets, fc='#98FB98', ec='#98FB98', alpha=0.4)
    plt.show()

if __name__ == "__main__":
    main()
