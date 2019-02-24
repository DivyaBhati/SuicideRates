import pandas as pd
import numpy as np

#Returns total suicides by age group for a inputted country
#return a dictionary (age ranges) of dictionaries (years:suicide rate)
#suicide rate is number out of 100,000 of the population for that age subset
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

#rawdata is a csv with the first column country name and remaining years
#works with most WHO data as long as you delete their weird erroneous empty columns and rows they put in
#return is a dictionary of the form year:value for the inputted country and data
def who_extract(rawdata, country):
	dict_list = rawdata.to_dict(orient='records')
	dict_country = {}
	for i in range(len(dict_list)):
		dict_country[dict_list[i]['Country'].strip()] = dict_list[i]
	data = dict_country[country]
	del data['Country']
	data = {int(k):round(v, 3) for k,v in data.items()}
	return(data)

#data is a dictionary of the form year:value
#suicides the return from age_group_data
#returns a list of lists that are all for the same years
#form is [[adjusted input data], [years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]
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

#suicide is return from age_group_data
#returns tuple of list of years and list of dictionaries of lists of the form age_range:list of suicide rates by year
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

#returns suicides in this form [[years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]]
def country_suicides(country):
	suicides = age_group_data(country)
	return(suicides_list_adjusted(suicides))

#fills in any missing data between given years
#return is a list
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

#gets list of lists of this form (all data indexed by the same year range):
#[[gdp], [years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]
def gdp_and_suicides(country):
	data = pd.read_csv("data/gdp.csv")
	return(something_and_suicides(country, who_extract(data, country)))

#gets list of lists of this form (all data indexed by the same year range):
#[[pollution], [years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]
def pollution_and_suicides(country):
	data = pd.read_csv("data/pollution.csv")
	return(something_and_suicides(country, who_extract(data, country)))

#gets list of lists of this form (all data indexed by the same year range):
#[[education index], [years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]
def education_and_suicides(country):
	data = pd.read_csv('data/education.csv')
	return(something_and_suicides(country, who_extract(data, country)))

#gets list of lists of this form (all data indexed by the same year range):
#[[internet usage rate], [years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]
def internet_and_suicides(country):
	data = pd.read_csv('data/internetusers.csv')
	return(something_and_suicides(country, who_extract(data, country)))

#gets list of lists of this form (all data indexed by the same year range):
#[[alcohol consumption], [years], [5-14 years], [15-24 years], [25-34 years], [35-54 years], [55-74 years], [75+ years], [Overall]]
def alcohol_and_suicides(country):
	data = pd.read_csv('data/alcohol.csv')
	return(something_and_suicides(country, who_extract(data, country)))

def all_and_suicides(input, country):
    input = input.lower()
    mapping = {
        "gdp": gdp_and_suicides(country),
        "pollution": pollution_and_suicides(country),
        "education": education_and_suicides(country),
        "internet": internet_and_suicides(country),
        "alcohol": alcohol_and_suicides(country)
    }
    return mapping[input]
