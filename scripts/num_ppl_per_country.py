import csv
import json

with open("data/WCA_export189_20230708T100008Z.tsv/WCA_export_Persons.tsv", "r", encoding="utf8") as text:
    tsv_reader = csv.reader(text, delimiter="\t")

    # Skip the first row, which is the header
    next(tsv_reader)

    data = {'country': [], 'incidence': []}

    for row in tsv_reader:
        (subid, name, countryID, gender, id) = row
        if countryID not in data['country']: 
            data['country'].append(countryID)
            data['incidence'].append(1)
        else:
            idx = data['country'].index(countryID)
            data['incidence'][idx]+=1

with open('data/data_num_ppl_per_country.json', 'w') as f:
    f.write(json.dumps(data))
    f.write('\n')