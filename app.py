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

class compare_form(FlaskForm):
    country = StringField(u'Country: ', validators=[Required()])
    factor = StringField(u'Factor: ', validators=[Required()])
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


#Run app
if __name__ == '__main__':
    app.run()
