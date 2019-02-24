import pandas as pd
import numpy as np
from collections import defaultdict

suicides = pd.read_csv("data/who_suicide_statistics.csv")
gdp = pd.read_csv("data/gdp/gdp.csv")


def age_group_data(country):
    country = suicides.loc[suicides['country'] == country]
    ages = {"75+ years": {}, "15-24 years":{}, "25-34 years": {}, "35-54 years":{}, "5-14 years":{}, "55-74 years":{}}
    for i in range(1979, 2016):
        year_data = country.loc[country['year'] == i]
        for index, row in year_data.iterrows():
            val = row['suicides_no'] / row['population'] * 100000
            ages[row['age']][i] = round(ages[row['age']].get(i, 0) + val, 2)
    return ages

def gdp_data():
	dict_list = gdp.to_dict(orient='records')
	gdp_dict_country = {}
	for i in range(len(dict_list)):
		gdp_dict_country[dict_list[i]['Country Name']] = dict_list[i]
	return(gdp_dict_country)
	
def gdp_data_country(country):
	return(gdp_data()[country])



