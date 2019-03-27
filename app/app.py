from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)
