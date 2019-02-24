import pandas as pd
import numpy as np
from data import age_group_data

#returns list of countries we will use on the sitre
#essentially checks if they are in every data set
def usable_countries():
	suicides = pd.read_csv('data/who_suicide_statistics.csv')
	alcohol = pd.read_csv('data/alcohol.csv')
	internet = pd.read_csv('data/internetusers.csv')
	education = pd.read_csv('data/education.csv')
	pollution = pd.read_csv('data/pollution.csv')
	gdp = pd.read_csv('data/gdp.csv')

	suilist = set(map(str.strip, suicides['country'].tolist()))
	alclist = set(map(str.strip, alcohol['Country'].tolist()))
	intlist = set(map(str.strip, internet['Country'].tolist()))
	edulist = set(map(str.strip, education['Country'].tolist()))
	pollist = set(map(str.strip, pollution['Country'].tolist()))
	gdplist = set(map(str.strip, gdp['Country'].tolist()))

	superlist = suilist.intersection(alclist, intlist, edulist, pollist, gdplist)
	return(list(superlist))

#im tired rip efficiency
def healthcare_data():
	datedict = {'Argentina':2016, 'Brazil':1988, 'Colombia':1993, 'Denmark':1973, 'Greece':1983, 'Iceland':1990, 'Israel':1995, 'Italy':1978,'Mexico':2012,'Singapore':1993,'Spain':1986,'Switzerland':1994,'Thailand':2002}
	start = -19
	end = 12
	for key, value in datedict.items():
		suicides = age_group_data(key)['Overall']
		endval = max(suicides.keys()) - value
		if endval > end:
			end = endval
		startval = min(suicides.keys()) - value
		if startval < start:
			start = startval

	newdict = {}
	findex = range(start, end)
	df = pd.DataFrame(index=datedict.keys(), columns=findex)

	for key, value in datedict.items():
		suicides = age_group_data(key)['Overall']
		for key1, val1 in suicides.items():
			df.at[key, key1 - value] = val1



	return(df)

print(healthcare_data().values.tolist())


