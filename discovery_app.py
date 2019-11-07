# -*- coding: utf-8 -*-

'''Project: Data Discovery App
Author: Connor Watson

This application built in Dash by Plotly allows the user to find
relationships between disparate data sets. It may not be clear,
but availability of data and accessability are not equal.
To solve this, we are creating an interactive journal article
which will help readers find their own relationships within
NYC data. '''

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data_file = 'C:\\Users\\watson\\Documents\\GitHub\\data_discovery_project\\datasets\\yearly_data.csv'
df = pd.read_csv(data_file, index_col=0)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_columns = list(df.columns)
df_columns.remove('year')
drop_options = [{'value':col, 'label':' '.join(col.lower().split('_'))} for col in df_columns]


def make_graph(graph_id, opts):
    return dcc.Graph(
        id=graph_id,
        figure={
            'data': [
                {'x': df['year'], 'y': df[opt], 'type': 'line'}#, 'name': 'SF'},
                for opt in opts
            ],
            'layout': {'title': 'Yearly Data'}
        },
        animate=False
    )

app.layout = html.Div(children=[
    html.H1(children='Data Discovery'),
    html.H3(children='Finding Relationships Amongst Disparate Data Sets'),
    html.Div(children='By: Connor Watson, Priyanka Racharla, and Keval Kavle'),

    html.Div(children='''
    In this application we seek to find relationships amongst data sets
    which seemingly have no relationship. 
    '''),
    dcc.Dropdown(
        id='dropdown-options',
        options=drop_options,
        value=['new_york_city_population'],
        multi=True
    ),
    html.Div(id='graph-1')
])

@app.callback(
    Output("graph-1", "children"),
    [Input("dropdown-options", "value")],
)
def update_options(options_selected):
    #options_selected is the list of dropdown options
    my_graph = make_graph('yearly-data', options_selected)
    return my_graph


def main():
    #for opt in drop_options:
    #    print(opt)
    pass
    
if __name__ == '__main__':
    main()
    app.run_server(debug=True)
