import json
import matplotlib.pyplot as plt
import numpy as np

with open('data/countries.json', 'r') as f:
    data_rel = json.load(f)

with open('data/data_num_ppl_per_country.json', 'r') as f:
    data_ppl = json.load(f)

tot_rel = [[], [], [], [], [], [], [], [], []]
arr_countries = []

for i in data_rel: 
    arr_countries.append(i[0])
for i in range(len(data_ppl['country'])):
    country = data_ppl['country'][i]
    num_ppl = data_ppl['incidence'][i]
    idx = arr_countries.index(country)
    tot_rel[0].append(country)
    for j in range(1,9):
        tot_rel[j].append(round(num_ppl*data_rel[idx][j] / 100))

with open('data/religions.json', 'w') as f:
    f.write(json.dumps(tot_rel))
    f.write('\n')

y = np.array([sum(tot_rel[1]), sum(tot_rel[2]), sum(tot_rel[3]), sum(tot_rel[4]), sum(tot_rel[5]), sum(tot_rel[6]), sum(tot_rel[7]), sum(tot_rel[8])])
mylabels = ['Christian: '+f'{sum(tot_rel[1])}', 'Muslim: '+f'{sum(tot_rel[2])}', 'Unaffiliated: '+f'{sum(tot_rel[3])}', 'Hindu: '+f'{sum(tot_rel[4])}', 'Buddhist: '+f'{sum(tot_rel[5])}', 'Folk Religion: '+f'{sum(tot_rel[6])}', 'Other Religion: '+f'{sum(tot_rel[7])}', 'Jewish: '+f'{sum(tot_rel[8])}']

fig, (ax1) = plt.subplots(1,figsize=(22,14))
ax1.pie(y, labels=mylabels)
ax1.legend(loc='best')
plt.title('Religion Breakdown for All WCA Competitors')
plt.savefig('pie_chart_religions')
plt.show()
