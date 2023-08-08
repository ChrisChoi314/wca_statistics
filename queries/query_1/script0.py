import json
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

with open('queries/query_1/data/country/API_SP.POP.TOTL_DS2_en_csv_v2_5695140.csv', 'r') as f:
    csv_reader = csv.reader(f)
    
    for i in range(5):
        next(csv_reader)
    
    data = {'country': [], 'population': []} 
    
    for row in csv_reader:
        print(row[0], row[-2])
        if row[0] != 'Not classified':
            data['country'].append(row[0])
            data['population'].append(int(row[-2]))

with open('queries/query_1/data/population1.json', 'w') as f:
    f.write(json.dumps(data))
    f.write('\n')
