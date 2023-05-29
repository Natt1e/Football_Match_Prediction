import pandas as pd

df = pd.read_csv('winRateDif.csv')

rateDif = df['difRate'].values
#print(rateDif)

dif = sum(rateDif) / len(rateDif)

print("Home wins are about {:.2f}% more likely than away wins".format(dif * 100))