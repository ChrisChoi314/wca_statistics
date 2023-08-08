import json
from tabulate import tabulate

with open('queries/query_1/data/ratios.json', 'r') as f:
    data_ratio = json.load(f)
with open('queries/query_1/data/competitors.json', 'r') as f:
    data_comp = json.load(f)
with open('queries/query_1/data/population.json', 'r') as f:
    data_pop = json.load(f)
data2 = [[], []]
for i in range(len(data_ratio['country'])):
    data2[0].append(data_ratio['country'][i])
    data2[1].append(data_ratio['ratio'][i])
table = []
length = len(data2[0]) 
rank = 1
for i in range(length):
    max_ratio = 0
    country = ''
    idx = 0
    pop = 0
    comp = 0
    for j in range(len(data2[0])):  
        if data2[1][j] >= max_ratio:
            idx = j
            max_ratio = data2[1][j]
            country = data2[0][j]
            comp = data_comp['incidence'][data_comp['country'].index(country)]
            pop = data_pop['population'][data_pop['country'].index(country)]
    entry = [rank, country, max_ratio, comp, pop]
    table += [entry]
    rank += 1
    del data2[0][idx]
    del data2[1][idx]
print(table)
head = ['#', 'Country', 'Ratio', 'Competitors', 'Population']

print(tabulate(table, headers=head, tablefmt="grid"))

with open("queries/query_1/data/output1.txt", 'w') as f:
    f.write(tabulate(table, headers=head, tablefmt="grid"))
