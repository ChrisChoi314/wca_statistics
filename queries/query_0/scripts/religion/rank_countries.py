import copy
from tabulate import tabulate
import json

with open("data/religions.json", "r") as f:
    data0 = json.load(f)
with open("data/data_num_ppl_per_country.json", "r") as f:
    data1 = json.load(f)

data = copy.deepcopy(data0)
countries = data0[0]
# assign data
tables = [
    [], [], [], [], [], [], [], [], []
]

for i in range(1, 9):
    for j in range(0, 10):
        max_val = max(data[i])
        max_idx = data[i].index(max_val)
        tables[i-1].append([j+1, data[0][max_idx], max_val, round(100*max_val/data1['incidence'][data1['country'].index(data[0][max_idx])])])
        del data[i][max_idx]
        del data[0][max_idx]
    data[0] = copy.deepcopy(countries)


# create header
head = ['Rank', 'Country', 'Number of Cubers', 'Percent of Population']

# display tables
print('Countries with most Christian Cubers (Top 10)')
print(tabulate(tables[0], headers=head, tablefmt="grid"))

print('Countries with most Muslim Cubers (Top 10)')
print(tabulate(tables[1], headers=head, tablefmt="grid"))

print('Countries with most Unaffiliated Cubers (Top 10)')
print(tabulate(tables[2], headers=head, tablefmt="grid"))

print('Countries with most Hindu Cubers (Top 10)')
print(tabulate(tables[3], headers=head, tablefmt="grid"))

print('Countries with most Buddhist Cubers (Top 10)')
print(tabulate(tables[4], headers=head, tablefmt="grid"))   

print('Countries with most Folk Religion Cubers (Top 10)')
print(tabulate(tables[5], headers=head, tablefmt="grid"))

print('Countries with most Other Religion Cubers (Top 10)')
print(tabulate(tables[6], headers=head, tablefmt="grid"))

print('Countries with most Jewish Cubers (Top 10)') 
print(tabulate(tables[7], headers=head, tablefmt="grid"))


with open('tables/tables.txt', 'w') as f:
    for i in range(0, 8):
        f.write(tabulate(tables[i], headers=head, tablefmt="grid"))