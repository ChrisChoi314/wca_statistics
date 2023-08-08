import json
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

with open('queries/query_1/data/population.json', 'r') as f:
    data_pop = json.load(f)

with open('queries/query_1/data/competitors.json', 'r') as f:
    data_comp = json.load(f)

data_ratio = {'country': [], 'ratio': []}

for i in range(len(data_comp['country'])):
    country = data_comp['country'][i]
    idx = data_pop['country'].index(country)
    data_ratio['country'].append(country)

    new_ratio = data_comp['incidence'][i]/data_pop['population'][idx]
    data_ratio['ratio'].append(new_ratio)
    print(country, new_ratio)

with open('queries/query_1/data/ratios.json', 'w') as f:
    f.write(json.dumps(data_ratio))
    f.write('\n')
