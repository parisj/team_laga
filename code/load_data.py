import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

zonen_30 = pd.read_csv("data/tempo-30-zonen.csv", sep=";")
begegnungszonen = pd.read_csv("data/begegnungszonen.csv", sep=";")
gemeindestrasse = pd.read_csv("data/gemeindestrassenplan.csv", sep=";")

zonen_30_js = json.loads(df['Geo Shape'][0])
data = np.array(js['coordinates'][0])
fig, ax = plt.subplots()
ax.plot(data[:, 0], data[:, 1], ls="-", marker="o")
fig.savefig("/tmp/test.png")
# breakpoint()
