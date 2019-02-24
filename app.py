from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, AnyOf
from flask_navigation import Navigation
import pandas as pd
import math
from data import *

app = Flask(__name__)
nav = Navigation(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'reallyreallyreallysecretkey'

countries = ['Ireland', 'Luxembourg', 'Canada', 'Belgium', 'Mongolia', 'Israel', 'Estonia', 'Greece', 'Mexico', 'Ukraine', 'Montenegro', 'United States of America', 'Jordan', 'Philippines', 'Russian Federation', 'Italy', 'Japan', 'Morocco', 'Poland', 'Saudi Arabia', 'Bulgaria', 'Turkey', 'Colombia', 'Tajikistan', 'Peru', 'Malaysia', 'United Arab Emirates', 'Haiti', 'Kuwait', 'Costa Rica', 'Lithuania', 'Thailand', 'Latvia', 'Austria', 'Brunei Darussalam', 'Portugal', 'Spain', 'Azerbaijan', 'South Africa', 'Georgia', 'Iceland', 'Seychelles', 'Guatemala', 'Fiji', 'Paraguay', 'Bahrain', 'Netherlands', 'Malta', 'Slovenia', 'Belize', 'Hungary', 'Cuba', 'Trinidad and Tobago', 'Norway', 'Mauritius', 'Romania', 'Dominica', 'Chile', 'Croatia', 'Guyana', 'Cyprus', 'Switzerland', 'Dominican Republic', 'Oman', 'Syrian Arab Republic', 'Armenia', 'Serbia', 'Sweden', 'Kazakhstan', 'Denmark', 'Argentina', 'Germany', 'Singapore', 'Qatar', 'Sri Lanka', 'Honduras', 'Zimbabwe', 'Bosnia and Herzegovina', 'France', 'Brazil', 'Finland', 'Australia', 'Uzbekistan', 'El Salvador', 'Uruguay', 'Sao Tome and Principe', 'Tunisia', 'New Zealand', 'Barbados', 'Nicaragua', 'Albania', 'Maldives', 'Belarus', 'Jamaica', 'Suriname', 'Ecuador', 'Panama', 'Iraq']
countries.sort()
factors = ['GDP', 'Education', 'Pollution', 'Alcohol', 'Internet']

class compare_form(FlaskForm):
    country = SelectField(label='Country', choices=[(i,i) for i in countries])
    factor = SelectField(label='Factor', choices=[(i,i) for i in factors])
    submit = SubmitField(u'Submit')

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    country = None
    factor = None
    form = compare_form()
    if form.validate_on_submit():
        country = form.country.data
        factor = form.factor.data
        country_data = all_and_suicides(factor, country)
        return render_template('compare.html', form=form, country=country, factor=factor, country_data=country_data)
    return render_template('compare.html', form=form, country=country, factor=factor)

@app.route('/healthcare', methods=['GET', 'POST'])
def healthcare():
    return render_template('graph.html')

#Run app
if __name__ == '__main__':
    app.run()
