import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from shapely.geometry import Polygon
from shapely.geometry import LineString

zonen_30 = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
begegnungszonen = pd.read_csv("data/begegnungszonen.csv", sep=";")
gemeindestrassen = pd.read_csv("data/gemeindestrassenplan.csv", sep=";")

r = 6371000

begegnungszonen_js = json.loads(gemeindestrassen['Geo Shape'][0])
data = np.array(begegnungszonen_js['coordinates'][0])

x = r_earth * np.sin(np.radians(data[:, 0])) * np.cos(np.radians(data[:, 1]))
y = r_earth * np.sin(np.radians(data[:, 0])) * np.sin(np.radians(data[:, 1]))
z = r_earth * np.cos(np.radians(data[:, 0]))

data = np.array([xyz for xyz in zip(x, y, z)])
line = Polygon(data)
print(line.area)
fig, ax = plt.subplots()
ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
fig.savefig("/tmp/test.png")

# breakpoint()
