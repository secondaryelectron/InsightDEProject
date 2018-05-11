# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os


from cassandra.cluster import Cluster

import config

cluster = Cluster(config.CASSANDRA_SERVER)
session = cluster.connect(config.CASSANDRA_NAMESPACE)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
		style={
            'textAlign': 'center',
			'fontSize': 18
        }
    )

#app = dash.Dash()

#app.layout = html.Div(children=[
#    html.H1(children='User Preference Over News Categories'),

#   html.Div(children='''
#        Dash: A web application framework for Python.
#   '''),

#    dcc.Graph(
#        id='example-graph',
#        figure={
#           'data': [
#                {'x': [1,2,3,4,5], 'y': countlist, 'type': 'bar', 'name': 'Counts'}
#            ],
#            'layout': {
#                'title': 'Dash Data Visualization'
#            }
#        }
#    )
#])

app = dash.Dash()
colors = {
    'background': '#7BFDBB',
    'text': '#7FDBFF'
}
app.layout = html.Div(children=[
	html.H1(
		children='NewsFinder',
		style={
            'textAlign': 'center',
			'fontSize': 40
        }
	),

	html.Div(
		children='Please enter User ID:',
		style={
			'fontSize': 32
        }
    ),
    dcc.Input(
		id='input-box', 
		type='text'
	),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit')
])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])

def update_output(n_clicks, value):
	if not value:
		return
	
    rows = session.execute('SELECT * FROM summary WHERE userid =\'{}\''.format(value))
	cate = []
	views = []
	materialized_rows = list(rows)
	n = len(materialized_rows)
	for i in range(n):
		cate.append(materialized_rows[i][2])
		views.append(materialized_rows[i][1])
	cate_rec = materialized_rows[0][2]
	print cate_rec

	news_rec = session.execute('SELECT * FROM news WHERE category = \'{}\' LIMIT 3'.format(cate_rec))
	materialized_news = list(news_rec)
	df = pd.DataFrame(materialized_news, columns=['Category','Published Date','Review Times','News ID','Source URL'])
	df = df[['News ID','Published Date','Category','Review Times','Source URL']]
	
	
	return html.Div([			
			html.Div([
				dcc.Graph(
					id='user-history',
					figure={
						'data':[{'x': cate, 'y':views, 'type':'bar', 'name':value}],
						'layout': {'title': 'User Views History','legend': {'x':0, 'y':1}}
						})
        			 ],
						style={'width': '49%', 'display': 'inline-block'}),

			html.Div([ 
					generate_table(df)
					], style={'width': '49%', 'display': 'inline-block'})
	])	

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]


for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=80,debug=True)
