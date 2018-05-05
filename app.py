# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from cassandra.cluster import Cluster

import config

cluster = Cluster(config.CASSANDRA_SERVER)
session = cluster.connect(config.CASSANDRA_NAMESPACE)

result = session.execute("SELECT * FROM demo1")

countlist=[]
for i in range(5):
	countlist.append(result[i].count)




app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='User Preference Over News Categories'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1,2,3,4,5], 'y': countlist, 'type': 'bar', 'name': 'Counts'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=80,debug=True)
