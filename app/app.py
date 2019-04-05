from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import requests
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import time
import os

app_flask = Flask(__name__)

app_dash = dash.Dash(__name__, server=app_flask, url_base_pathname='/dashapp/')
app_dash.scripts.config.serve_locally = False

# Use this to counter warning
## From stack-overflow:
### Flask-SQLAlchemy has its own event notification system that gets layered on top of SQLAlchemy. 
### To do this, it tracks modifications to the SQLAlchemy session. 
### This takes extra resources, so the option SQLALCHEMY_TRACK_MODIFICATIONS allows you to disable the 
### modification tracking system.
app_flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#################################################
# Database Setup
#################################################

app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/zdat.sqlite"
db = SQLAlchemy(app_flask)

#################################################
# Declare Model (Table schema)
#################################################

class HousingData(db.Model):
	__tablename__ = 'zilloData'
	index = db.Column(db.BIGINT, primary_key=True)
	RegionName = db.Column(db.TEXT)
	Date = db.Column(db.TEXT)
	Number_of_Listings = db.Column(db.FLOAT)
	Year = db.Column(db.TEXT)
	Month = db.Column(db.TEXT)
	Median_sqft_Value = db.Column(db.FLOAT)
	
	def __repr__(self):
		return '<Region %r>' % self.RegionName

# Code from sqlite3 when call .schema within console
# CREATE TABLE IF NOT EXISTS "zilloData" (
# 	"index" BIGINT, 
# 	"RegionName" TEXT, 
# 	"Date" TEXT, 
# 	"Number_of_Listings" FLOAT, 
# 	"Year" TEXT, 
# 	"Month" TEXT, 
# 	"Median_sqft_Value" FLOAT
# );
# CREATE INDEX "ix_zilloData_index" ON "zilloData" ("index");
##################################################


#Application routes
@app_flask.route('/')
@app_flask.route('/index')
def index():
    return render_template('home.html')

@app_flask.route('/charts')
def charts():
    return render_template('charts.html')

@app_flask.route('/map')
def map():
    return render_template('map.html')

@app_flask.route('/test')
def test():
	return render_template('index.html')

@app_flask.route('/about')
def about():
    return render_template('about.html')

@app_flask.route('/data/inventory/<year>')
def yearly_inventory(year):
	""" Get number of listings and inventory for a given year 
		Return as a json dictionary """
	sel = [
		HousingData.RegionName,
		HousingData.Year,
		HousingData.Month,
		HousingData.Number_of_Listings,
		HousingData.Median_sqft_Value
	]
	
	results = db.session.query(*sel).filter(HousingData.Year == year).all()

	json_results = []
	yearly_housing_data = {}

	for result in results:
		yearly_housing_data = {}
		yearly_housing_data['RegionName'] = result[0]
		yearly_housing_data['Year'] = result[1]
		yearly_housing_data['Month'] = result[2]
		yearly_housing_data['Number_of_Listings'] = result[3]
		yearly_housing_data['Median_sqft_Value'] = result[4]
		json_results.append(yearly_housing_data)

	print(json_results)
	return jsonify(json_results)

@app_flask.route('/data/inventory/<month>/<year>')
def monthly_inventory(year,month):
	""" Get number of listings and inventory for a given year and month
		Return as a json dictionary """
	sel = [
		HousingData.RegionName,
		HousingData.Year,
		HousingData.Month,
		HousingData.Number_of_Listings,
		HousingData.Median_sqft_Value
	]
	
	results = db.session.query(*sel).filter(HousingData.Year == year, HousingData.Month == month).all()

	json_results = []
	monthly_housing_data = {}

	for result in results:
		monthly_housing_data = {}
		monthly_housing_data['RegionName'] = result[0]
		monthly_housing_data['Year'] = result[1]
		monthly_housing_data['Month'] = result[2]
		monthly_housing_data['Number_of_Listings'] = result[3]
		monthly_housing_data['Median_sqft_Value'] = result[4]
		json_results.append(monthly_housing_data)

	print(json_results)
	return jsonify(json_results)

@app_flask.route('/data/geo_json')
def geo_json():
	# pull geojson file, load into json
	res = requests.get('https://raw.githubusercontent.com/crieck/housing-using-zillow-ZHVI/feature-map/map-features/leaflet-mn-cities/static/js/mn-city-bounds.geojson')
	print(res)
	response = res.json()
	print(response)

	# setting values to -1 to allow for adding data in javascript code when updating map
	for place in response['features']:
		place['properties']['Number_of_Listings'] = -1
		place['properties']['Median_sqft_Value'] = -1	

	return jsonify(response)

#################################################
# Dash setup and data
#################################################

@app_flask.route('/zillow_dashboard') 
def render_dashboard():
    return flask.redirect('/dashapp')

df=pd.read_sql_query('select * from zilloData;',db.session.bind)

app_dash.layout = html.Div([
    html.H2('Zillo Data'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': i, 'value': i} for i in df['RegionName']],
        value='Minneapolis'
    ),
    dcc.Graph(id='1graph'),
    dcc.Graph(id='2graph')
], className="container")

@app_dash.callback(Output('1graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = df[df['RegionName'] == selected_dropdown_value]
    return {
        'data': [{
            'x': dff.Date,
            'y': dff.Number_of_Listings,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
            'layout': {
                'title': 'Number_of_Listings'
            }

    }
@app_dash.callback(Output('2graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = df[df['RegionName'] == selected_dropdown_value]
    return {
        'data': [{
            'x': dff.Date,
            'y': dff.Median_sqft_Value,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
            'layout': {
                'title': 'Median_sqft_Value'
            }
    }

if __name__ == '__main__':
    app_flask.run(debug=True)