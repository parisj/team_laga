import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

zonen_30 = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
begegnungszonen = pd.read_csv("data/begegnungszonen.csv", sep=";")
gemeindestrassen = pd.read_csv("data/gemeindestrassenplan.csv", sep=";")

begegnungszonen_js = json.loads(gemeindestrassen['Geo Shape'][0])
data = np.array(begegnungszonen_js['coordinates'][0])
fig, ax = plt.subplots()
ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
fig.savefig("/tmp/test.png")
# breakpoint()
