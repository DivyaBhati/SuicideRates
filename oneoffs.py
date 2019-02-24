import pandas as pd

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


