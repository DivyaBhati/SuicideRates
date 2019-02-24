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

def something_and_suicides(data, suicide):
	data_years = data.keys()
	suicide_years = suicide['5-14 years'].keys()
	mindata = min(data_years)
	minsuic = min(suicide_years)
	maxdata = max(data_years)
	maxsuic = max(suicide_years) 
	start_year = mindata if mindata > minsuic else minsuic
	end_year = maxdata if maxdata < maxsuic else maxsuic

	years = range(start_year, end_year)


def interpolate_list(start_year, end_year, data):
	datalist = []
	for i in range(start_year, end_year):
		if i in data_years:
			datalist.append(data[i])
		else:
			datalist.append(np.nan)

	datalist = pd.Series(datalist).interpolate().tolist()
	return(datalist)

