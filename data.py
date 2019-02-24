import pandas as pd
import numpy as np
from collections import defaultdict

data = pd.read_csv("who_suicide_statistics.csv")
usa = data.loc[data['country'] == "United States of America"]

#Returns total suicides by age group for a country
def ageGroupData(country):
    ages = {"5-14 years":{}, "15-24 years":{}, "25-34 years": {}, "35-54 years":{}, "55-74 years":{}, "75+ years": {}}
    for i in range(1979, 2016):
        year_data = country.loc[country['year'] == i]
        for index, row in year_data.iterrows():
            val = row['suicides_no'] / row['population'] * 100000
            ages[row['age']][i] = round(ages[row['age']].get(i, 0) + val, 2)
    return ages

#Returns data in list format for graphing
def dataForGraphing(country):
    ages = ageGroupData(country)
    lists = []
    for group in ages:
        curr = []
        for key, val in ages[group].items():
            curr.append(val)
        lists.append(curr)
    return lists

years = ""
for i in range(1979, 2016):
    years += "\'"+str(i)+"\', "
print(years)

print(dataForGraphing(usa))
