import pandas as pd
import numpy as np
from collections import defaultdict

suicides = pd.read_csv("data/who_suicide_statistics.csv")
gdp = pd.read_csv("data/gdp/gdp.csv")


<<<<<<< HEAD
#Returns total suicides by age group for a country
def ageGroupData(country):
    ages = {"5-14 years":{}, "15-24 years":{}, "25-34 years": {}, "35-54 years":{}, "55-74 years":{}, "75+ years": {}}
=======
def age_group_data(country):
    country = suicides.loc[suicides['country'] == country]
    ages = {"75+ years": {}, "15-24 years":{}, "25-34 years": {}, "35-54 years":{}, "5-14 years":{}, "55-74 years":{}}
>>>>>>> ec2dbf132e211244eb7b63a8847694a053f05ca9
    for i in range(1979, 2016):
        year_data = country.loc[country['year'] == i]
        for index, row in year_data.iterrows():
            val = row['suicides_no'] / row['population'] * 100000
            ages[row['age']][i] = round(ages[row['age']].get(i, 0) + val, 2)
    return ages

<<<<<<< HEAD
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

def gdp_data():
	dict_list = gdp.to_dict(orient='records')
	gdp_dict_country = {}
	for i in range(len(dict_list)):
		gdp_dict_country[dict_list[i]['Country Name']] = dict_list[i]
	return(gdp_dict_country)

def gdp_data_country(country):
	return(gdp_data()[country])

print(dataForGraphing(usa))
=======
def gdp_data():
	dict_list = gdp.to_dict(orient='records')
	gdp_dict_country = {}
	for i in range(len(dict_list)):
		gdp_dict_country[dict_list[i]['Country Name']] = dict_list[i]
	return(gdp_dict_country)

def gdp_data_country(country):
	return(gdp_data()[country])



>>>>>>> ec2dbf132e211244eb7b63a8847694a053f05ca9
