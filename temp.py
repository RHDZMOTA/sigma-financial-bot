import numpy as np
import json

a = np.load("name2desc.npy")


mexican_tickers = a.item()

with open("data/stocks/mexican_tickers.json", "w") as file:
    file.write(json.dumps(mexican_tickers))
