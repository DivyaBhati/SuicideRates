import pandas as pd
import numpy as np


suicides = pd.read_csv("data/who_suicide_statistics.csv")
gdp = pd.read_csv("data/gdp/gdp.csv")


#Returns total suicides by age group for a country
def ageGroupData(country):
    data = suicides.loc[suicides['country'] == country]
    ages = {"5-14 years":{}, "15-24 years":{}, "25-34 years": {}, "35-54 years":{}, "55-74 years":{}, "75+ years": {}, "Overall": {}}
    for i in range(1979, 2016):
        total_pop = 0
        total_suicides = 0
        year_data = data.loc[data['year'] == i]
        for index, row in year_data.iterrows():
            val = row['suicides_no'] / row['population'] * 100000
            total_suicides = total_suicides + row['suicides_no']
            total_pop = total_pop + row['population']
            ages[row['age']][i] = round(ages[row['age']].get(i, 0) + val, 2)
        ages['Overall'][i] = round(total_suicides / total_pop * 100000, 2)
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

def gdp_data():
	dict_list = gdp.to_dict(orient='records')
	gdp_dict_country = {}
	for i in range(len(dict_list)):
		gdp_dict_country[dict_list[i]['Country Name']] = dict_list[i]
	return(gdp_dict_country)

def gdp_data_country(country):
	data = gdp_data()[country]
	del data['Country Name']
	del data['Country Code']
	del data['Indicator Name']
	del data['Indicator Code']
	data = {int(k):v for k,v in data.items()}
	return(data)

def something_and_suicides(country, data):
	suicide = ageGroupData(country)
	data_years = data.keys()
	suicide_years = suicide['5-14 years'].keys()
	mindata = min(data_years)
	minsuic = min(suicide_years)
	maxdata = max(data_years)
	maxsuic = max(suicide_years) 
	start_year = mindata if mindata > minsuic else minsuic
	end_year = maxdata if maxdata < maxsuic else maxsuic

	years = list(range(start_year, end_year + 1))
	something = interpolate_dict(start_year, end_year, data)
	kids = interpolate_dict(start_year, end_year, suicide['5-14 years'])
	teens = interpolate_dict(start_year, end_year, suicide['15-24 years'])
	adults = interpolate_dict(start_year, end_year, suicide['25-34 years'])
	middleage = interpolate_dict(start_year, end_year, suicide['35-54 years'])
	olds = interpolate_dict(start_year, end_year, suicide['55-74 years'])
	geriatrics = interpolate_dict(start_year, end_year, suicide['75+ years'])
	overall = interpolate_dict(start_year, end_year, suicide['Overall'])

	return([years, something, kids, teens, adults, middleage, olds, geriatrics, overall])

def suicides_list(country):
	suicide = ageGroupData(country)
	suicide_years = suicide['5-14 years'].keys()
	start_year = min(suicide_years)
	end_year = max(suicide_years)

	years = list(range(start_year, end_year + 1))
	kids = interpolate_dict(start_year, end_year, suicide['5-14 years'])
	teens = interpolate_dict(start_year, end_year, suicide['15-24 years'])
	adults = interpolate_dict(start_year, end_year, suicide['25-34 years'])
	middleage = interpolate_dict(start_year, end_year, suicide['35-54 years'])
	olds = interpolate_dict(start_year, end_year, suicide['55-74 years'])
	geriatrics = interpolate_dict(start_year, end_year, suicide['75+ years'])
	overall = interpolate_dict(start_year, end_year, suicide['Overall'])

	return([years, kids, teens, adults, middleage, olds, overall])

def interpolate_dict(start_year, end_year, data):
	datalist = []
	data_years = data.keys()
	for i in range(start_year, end_year + 1):
		if i in data_years:
			datalist.append(data[i])
		else:
			datalist.append(np.nan)

	datalist = pd.Series(datalist).interpolate(method='linear').tolist()
	return(datalist)

print(something_and_suicides('United States of America', gdp_data_country('United States of America')))