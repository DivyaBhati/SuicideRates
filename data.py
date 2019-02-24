import pandas as pd
import numpy as np

#Returns total suicides by age group for a country
def age_group_data(country):
    suicides = pd.read_csv("data/who_suicide_statistics.csv")
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

def who_extract(rawdata, country):
	dict_list = rawdata.to_dict(orient='records')
	dict_country = {}
	for i in range(len(dict_list)):
		dict_country[dict_list[i]['Country'].strip()] = dict_list[i]
	data = dict_country[country]
	del data['Country']
	data = {int(k):round(v, 3) for k,v in data.items()}
	return(data)

def gdp_data(country):
	data = pd.read_csv("data/gdp.csv")
	return(who_extract(data, country))


def pollution_data(country):
	data = pd.read_csv("data/pollution.csv")
	return(who_extract(data, country))


def education_data(country):
	data = pd.read_csv('data/education.csv')
	return(who_extract(data, country))

def internet_data(country):
	data = pd.read_csv('data/internetusers.csv')
	return(who_extract(data, country))


def something_and_suicides(country, data):
	suicides = age_group_data(country)
	data_years = data.keys()
	suicide_years = suicides['5-14 years'].keys()
	mindata = min(data_years)
	minsuic = min(suicide_years)
	maxdata = max(data_years)
	maxsuic = max(suicide_years) 
	start_year = mindata if mindata > minsuic else minsuic
	end_year = maxdata if maxdata < maxsuic else maxsuic	
	something = interpolate_dict(start_year, end_year, data)
	return([something] + suicides_list_adjusted(suicides, start_year, end_year))

def suicides_list_adjusted(suicide, start_year=0, end_year=0):
	if start_year == 0:
		suicide_years = suicide['5-14 years'].keys()
		start_year = min(suicide_years)
		end_year = max(suicide_years)
	years = list(range(start_year, end_year + 1))
	suicides_list = []
	for key in suicide.keys():
		suicides_list.append(interpolate_dict(start_year, end_year, suicide[key]))
	return([years] + suicides_list)

def country_suicides(country):
	suicides = age_group_data(country)
	return(suicides_list_adjusted(suicides))

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

def gdp_and_suicides(country):
	return(something_and_suicides(country, gdp_data(country)))

def pollution_and_suicides(country):
	return(something_and_suicides(country, pollution_data(country)))

def education_and_suicides(country):
	return(something_and_suicides(country, education_data(country)))

def internet_and_suicides(country):
	return(something_and_suicides(country, internet_data(country)))