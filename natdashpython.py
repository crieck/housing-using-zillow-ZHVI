#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

import sqlite3


# In[2]:


server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')
conn=sqlite3.connect('documents/homeworkarchive/p3d/zdat.sqlite')
c=conn.cursor()
c.execute('select * from zilloData;')


# In[3]:


df=pd.read_sql_query('select * from zilloData;',conn)


# In[4]:


df.head()


# In[5]:


app = dash.Dash('app', server=server)
app.scripts.config.serve_locally = False
server = app.server


# In[6]:


app.layout = html.Div([
    html.H2('Zillo Data'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': i, 'value': i} for i in df['RegionName']],
        value='Minneapolis'
    ),
    dcc.Graph(id='1graph'),
    dcc.Graph(id='2graph')
], className="container")

@app.callback(Output('1graph', 'figure'),
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
@app.callback(Output('2graph', 'figure'),
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


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




