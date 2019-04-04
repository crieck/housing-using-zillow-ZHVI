{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import dash\n",
    "from dash.dependencies import Input, Output\n",
    "import dash_core_components as dcc\n",
    "import dash_html_components as html\n",
    "\n",
    "import flask\n",
    "import pandas as pd\n",
    "import time\n",
    "import os\n",
    "\n",
    "import sqlite3"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<sqlite3.Cursor at 0x113ddcea0>"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "server = flask.Flask('app')\n",
    "server.secret_key = os.environ.get('secret_key', 'secret')\n",
    "conn=sqlite3.connect('documents/homeworkarchive/p3d/zdat.sqlite')\n",
    "c=conn.cursor()\n",
    "c.execute('select * from zilloData;')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "df=pd.read_sql_query('select * from zilloData;',conn)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>index</th>\n",
       "      <th>RegionName</th>\n",
       "      <th>Date</th>\n",
       "      <th>Number_of_Listings</th>\n",
       "      <th>Year</th>\n",
       "      <th>Month</th>\n",
       "      <th>Median_sqft_Value</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>Minneapolis</td>\n",
       "      <td>2013-01</td>\n",
       "      <td>1082.0</td>\n",
       "      <td>2013</td>\n",
       "      <td>01</td>\n",
       "      <td>151.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>Saint Paul</td>\n",
       "      <td>2013-01</td>\n",
       "      <td>726.0</td>\n",
       "      <td>2013</td>\n",
       "      <td>01</td>\n",
       "      <td>108.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>Rochester</td>\n",
       "      <td>2013-01</td>\n",
       "      <td>435.0</td>\n",
       "      <td>2013</td>\n",
       "      <td>01</td>\n",
       "      <td>141.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>Duluth</td>\n",
       "      <td>2013-01</td>\n",
       "      <td>532.0</td>\n",
       "      <td>2013</td>\n",
       "      <td>01</td>\n",
       "      <td>141.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>Bloomington</td>\n",
       "      <td>2013-01</td>\n",
       "      <td>190.0</td>\n",
       "      <td>2013</td>\n",
       "      <td>01</td>\n",
       "      <td>149.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   index   RegionName     Date  Number_of_Listings  Year Month  \\\n",
       "0      0  Minneapolis  2013-01              1082.0  2013    01   \n",
       "1      1   Saint Paul  2013-01               726.0  2013    01   \n",
       "2      2    Rochester  2013-01               435.0  2013    01   \n",
       "3      3       Duluth  2013-01               532.0  2013    01   \n",
       "4      4  Bloomington  2013-01               190.0  2013    01   \n",
       "\n",
       "   Median_sqft_Value  \n",
       "0              151.0  \n",
       "1              108.0  \n",
       "2              141.0  \n",
       "3              141.0  \n",
       "4              149.0  "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = dash.Dash('app', server=server)\n",
    "app.scripts.config.serve_locally = False\n",
    "server = app.server"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "app.layout = html.Div([\n",
    "    html.H2('Zillo Data'),\n",
    "    dcc.Dropdown(\n",
    "        id='my-dropdown',\n",
    "        options=[{'label': i, 'value': i} for i in df['RegionName']],\n",
    "        value='Minneapolis'\n",
    "    ),\n",
    "    dcc.Graph(id='1graph'),\n",
    "    dcc.Graph(id='2graph')\n",
    "], className=\"container\")\n",
    "\n",
    "@app.callback(Output('1graph', 'figure'),\n",
    "              [Input('my-dropdown', 'value')])\n",
    "\n",
    "def update_graph(selected_dropdown_value):\n",
    "    dff = df[df['RegionName'] == selected_dropdown_value]\n",
    "    return {\n",
    "        'data': [{\n",
    "            'x': dff.Date,\n",
    "            'y': dff.Number_of_Listings,\n",
    "            'line': {\n",
    "                'width': 3,\n",
    "                'shape': 'spline'\n",
    "            }\n",
    "        }],\n",
    "            'layout': {\n",
    "                'title': 'Number_of_Listings'\n",
    "            }\n",
    "\n",
    "    }\n",
    "@app.callback(Output('2graph', 'figure'),\n",
    "              [Input('my-dropdown', 'value')])\n",
    "\n",
    "def update_graph(selected_dropdown_value):\n",
    "    dff = df[df['RegionName'] == selected_dropdown_value]\n",
    "    return {\n",
    "        'data': [{\n",
    "            'x': dff.Date,\n",
    "            'y': dff.Median_sqft_Value,\n",
    "            'line': {\n",
    "                'width': 3,\n",
    "                'shape': 'spline'\n",
    "            }\n",
    "        }],\n",
    "            'layout': {\n",
    "                'title': 'Median_sqft_Value'\n",
    "            }\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"app\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: Do not use the development server in a production environment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [04/Apr/2019 18:18:55] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:18:56] \"GET /_dash-dependencies HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:18:56] \"GET /_dash-layout HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:18:56] \"POST /_dash-update-component HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:18:56] \"POST /_dash-update-component HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:19:06] \"POST /_dash-update-component HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:19:06] \"POST /_dash-update-component HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:19:22] \"POST /_dash-update-component HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [04/Apr/2019 18:19:22] \"POST /_dash-update-component HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.run_server(debug=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 2",
   "language": "python",
   "name": "python2"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.15"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
