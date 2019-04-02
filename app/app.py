from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlalchemy

app = Flask(__name__)

# Use this to counter warning
## From stack-overflow:
### Flask-SQLAlchemy has its own event notification system that gets layered on top of SQLAlchemy. 
### To do this, it tracks modifications to the SQLAlchemy session. 
### This takes extra resources, so the option SQLALCHEMY_TRACK_MODIFICATIONS allows you to disable the 
### modification tracking system.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/zdat.sqlite"
db = SQLAlchemy(app)

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
@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data/inventory/<year>')
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

@app.route('/data/inventory/<month>/<year>')
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

if __name__ == '__main__':
    app.run(debug=True)
