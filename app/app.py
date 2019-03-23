from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/dashboard/')
def projects():
    return 'The dashboard page'