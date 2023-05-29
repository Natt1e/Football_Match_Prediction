import os
import csv


path = "./finalData"
files = os.listdir(path)
allData = []
count = 0
for file in files:
    f = path + "/" + file
    with open(f, "r", encoding='utf-8', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            allData.append(row)
headers = ['fightRateDif', 'fightGoalDif', 'recentRateDif', 'recentGoalDif', 'leagueRateDif', 'leagueGoapDif',
               'supportDif', 'result']
with open('matchData.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for d in allData:
        float_list = [float(x) for x in d]
        zeroSum = sum(abs(i) < 0.0001 for i in float_list)
        if zeroSum >= 4:
            count += 1
            continue
        elif sum(i < 0 for i in float_list) >= 6 and float_list[7] >= 0:
            print("unbelievable")
            continue
        elif sum(i > 0 for i in float_list) >= 6 and float_list[7] <= 0:
            print("NO")
            continue
        else:
            writer.writerow(d)
print(count)

path = './winRateData'
files = os.listdir(path)
allData = []
for file in files:
    f = path + "/" + file
    with open(f, "r", encoding='utf-8', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            allData.append(row)
headers = ['teamName', 'homeRate', 'awayRate', 'difRate']
names = []
with open('winRateDif.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for d in allData:
        if d[0] not in names:
            writer.writerow(d)
            names.append(d[0])
        #else:
            #print("%s duplicate" %d[0])
