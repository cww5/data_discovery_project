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
data_path = 'C:\\Users\\watson\\Documents\\GitHub\\data_discovery_project\\datasets\\'
data_file = data_path + 'yearly_data.csv'
stan_file = data_path + 'yearly_stan_data.csv'
df = pd.read_csv(stan_file, index_col=0)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_columns = list(df.columns)
df_columns.remove('year')
drop_options = [{'value':col, 'label':' '.join(col.lower().split('_'))} for col in df_columns]


def make_graph(graph_id, opts):
    return dcc.Graph(
        id=graph_id,
        figure={
            'data': [
                {'x': df['year'], 'y': df[opt], 'type': 'line', 'name': opt}
                for opt in opts
            ],
            'layout': {'title': 'Yearly Data', 'legend':{'orientation':'h'}}
        },
        animate=False
    )

app.layout = html.Div(children=[
    html.H1(children='Data Discovery'),
    html.H3(children='Finding Relationships Amongst Disparate Data Sets'),
    html.Div(children='By: Connor Watson, Priyanka Racharla, and Keval Kavle'),

    html.Div(children='''
    In this application we seek to find relationships amongst data sets
    which seemingly have no relationship. Thanks to recent efforts, we have
    access to lots of New York City data, and we intend to use data-driven story
    telling to inform the user of yearly trends.
    '''),
    html.Br(),

    html.Div(children='''
    The growth of the human population seems to keep increasing as time
    goes on. As the Internet has boomed, NYC has become more of a hub
    for both jobs and technology. With the increase in population comes
    an increase in effect on the environment as well. People joke about
    the 'dirty Hudson River', but in actuality, the condition of NYC and
    our Earth is no joke.
    '''),
    html.Br(),
    
    html.Div(children='''
    Within our findings, we can see that NYC's population has very clearly
    been increasing. Using the tool below, you can discover this trend
    yourself. It may also be interesting to compare the constant increase
    in population with the trends in other attributes of our data set
    as well.
    '''),
    html.Br(),

    html.Div(children='''
    One important discovery is that even though more and more people have
    populated NYC, it seems there is an inverse effect on the amount of
    water consumed per year in millions of gallons per day. After 1990,
    it seems as though there has been a general decline in the amount
    of water consumed per day. Could this be thanks to the realization
    that we are making a negative impact on the environment? If you select
    the 'schoolorganictons' attribute, you can clearly see that more tons
    of organic waste has been collected from schools, pointing to the
    acknowledgement by the Department of Education. What else can you discover?
    '''),
    html.Br(),

    html.Div('''
    NOTE: This graph is NOT to scale. All data points have been standardized
    to fall in the range [0,1]. This graph allows you to see the overall trends.
    '''),
    html.Br(),
    
    dcc.Dropdown(
        id='dropdown-options',
        options=drop_options,
        value=['new_york_city_population',
                'nyc_consumption_million_gallons_per_day',
                #'number_of_indoor_complaints',
                #'REFUSETONSCOLLECTED',
                #'PAPERTONSCOLLECTED',
                #'RESORGANICSTONS',
                #'SCHOOLORGANICTONS'
                ],
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
