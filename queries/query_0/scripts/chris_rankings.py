import csv
import json
from tabulate import tabulate

names = ['Chris', 'Christian', 'Christopher', 'Kris', 'Kristopher']
#names = ['Chris']
names = ['Christian']
names = ['Park', 'Bak', 'Pak']
names = ['Fan']
# names = ['Choi', 'Chey', 'Choe', 'Choy', 'Chwe', 'Che',]# 'Cho', 'Sho', 'Qoi', 'Qoy', 'Qo', 'Qhey', 'Qu', 'Qoy', 'Oy', 'Oi', 'Ci', 'Cy', 'Hy', 'Hoi', 'Hui', 'Xo', 'Xoi', 'Xi', 'X', 'C', 'Ch', 'Q', 'Quan', 'Chung', 'Chong', 'Chang']
names = ['Choi']
names = ['Antu', 'Anta']
names = ['Mahesh', 'Magesh']
names = ['Mageshwaran']
names = ['Aaron', 'Aron']
names = ['Alex', 'Alexander', 'Alexey', 'Alexei']
names = ['Parker']
names = ['Wang']
names = ['Max', 'Maks', 'Maximillian']
names = ['Donna']
events_to_ignore = ['333mbo', '333ft', 'magic', 'mmagic']

with open("data/WCA_export189_20230708T100008Z.tsv/WCA_export_Persons.tsv", "r", encoding="utf8") as text:
    tsv_reader = csv.reader(text, delimiter="\t")
    next(tsv_reader)

    chris_ids = [[],[]]

    for row in tsv_reader:
        (subid, name, countryID, gender, id) = row
        effective_name = name
        if ' (' in name:
            effective_name = name[:name.find(' (')]
        first_name = effective_name.split(' ')[0]
        last_name = effective_name.split(' ')[-1]
        if first_name in names:
            #chris_ids[0].append(id)
            #chris_ids[1].append(name)
        # if first_name[:4] in names:
        #if last_name in names or first_name in names:
        #if last_name in names:
            chris_ids[0].append(id)
            chris_ids[1].append(name)

data1 = [[], [], []]
with open("data/WCA_export189_20230708T100008Z.tsv/WCA_export_RanksSingle.tsv", "r", encoding="utf8") as text:
    tsv_reader = csv.reader(text, delimiter="\t")
    next(tsv_reader)
    for row in tsv_reader:
        (personId, eventId, best, worldRank, continentRank, countryRank) = row
        if personId in chris_ids[0]:
            data1[0].append(personId)
            data1[1].append(eventId)
            data1[2].append(worldRank)

data2 = [[], []]
with open("data/WCA_export189_20230708T100008Z.tsv/WCA_export_Events.tsv", "r", encoding="utf8") as text:
    tsv_reader = csv.reader(text, delimiter="\t")
    next(tsv_reader)
    for row in tsv_reader:
        (id, cellName, format, name, rank) = row
        if id not in events_to_ignore:
            data2[0].append(id)
            data2[1].append(cellName)
    
table = []
for j in range(len(data2[0])):
    event_rankings = []
    ranking = 10000000000
    for i in range(len(data1[0])):
        if data1[1][i] == data2[0][j]:
            if len(event_rankings) == 0 or ranking >= int(data1[2][i]):
                ranking = int(data1[2][i])
                event_rankings = [j + 1, data2[1][j], f'{chris_ids[1][chris_ids[0].index(data1[0][i])]} - {data1[0][i]}', ranking]
    table += [event_rankings]
print(table)
head = ['#', 'Event', 'Donna', 'Rank']

print(tabulate(table, headers=head, tablefmt="grid"))