# -*- coding: utf-8 -*-

'''Project: Data Discovery App
Authors: Connor Watson, Priyanka Racharla, Keval Kavle

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
num_file = data_path + 'yearly_numeric_data.csv'
stan_file = data_path + 'yearly_stan_data.csv'
pri_env_comp = data_path + 'pri_env_complaints_by_borough.csv'
num_df = pd.read_csv(num_file, index_col=0)
num_df['year'] = num_df['year'].astype(int)
stan_df = pd.read_csv(stan_file, index_col=0)

# df_columns apply for both num_df and stan_df
df_columns = list(stan_df.columns)
df_columns.remove('year')
drop_options = [{'value':col, 'label':' '.join(col.lower().split('_'))} for col in df_columns]

full_df = num_df[num_df.columns[num_df.notnull().all()]]
years = sorted(full_df['year'].values)

final_environComplaint = pd.read_csv(pri_env_comp)
final_environComplaint['Date_Received'] = pd.to_datetime(final_environComplaint['Date_Received'])

def make_graph(graph_id, opts, df, title):
    return dcc.Graph(
        id=graph_id,
        figure={
            'data': [
                {'x': df['year'], 'y': df[opt], 'type': 'line', 'name': opt}
                for opt in opts
            ],
            'layout': {'title': title, 'legend':{'orientation':'h', 'y':-0.20},
                       'xaxis':{'title':'year'},'yaxis':{'title':'trend'}}
        },
        animate=False
    )

def make_scatter(graph_id, x_axis, y_axis, df, title, mode='markers'):
    xp = x_axis.split('_')
    yp = y_axis.split('_')
    if len(xp) > 1:
        x_title = ' '.join(xp[:4])
    else:
        x_title = xp[0]
    if len(yp) > 1:
        y_title = ' '.join(yp[:4])
    else:
        y_title = yp[0]
    
    return dcc.Graph(
        id=graph_id,
        figure={
            'data': [
                {'x': df[x_axis], 'y': df[y_axis], 'mode':mode,
                 'text':df['year']}
            ],
            'layout': {'title': title, 'legend':{'orientation':'h'},
                       'xaxis':{'title':x_title},'yaxis':{'title':y_title}}
        },
        animate=False
    )

import plotly.graph_objects as go

def make_heatmap(graph_id, z_data, x_data, y_data, title):
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_data,
        y=y_data,
        colorscale='RdBu', zmid=0)
    )
    graph = dcc.Graph(
        id=graph_id,
        figure=fig
    )
    return graph

def make_bar(nm, xdata, ydata):
    my_bar = go.Bar(
        name=nm,
        x=xdata,
        y=ydata,
    )
    return my_bar

borolist = ['Brooklyn', 'Manhattan', 'Queens', 'Bronx', 'Staten Island']


def make_stacked_bars(df, year, comp_types, num_comps):
    fig = go.Figure(
        data=[
            make_bar(comp_types[i], borolist, num_comps[i]) for i in range(len(comp_types))
        ]
    )
    fig.update_layout(
        title="Overall " + str(year) + " Complaint Types by Borough",
        xaxis_title="Boroughs",
        yaxis_title= "Number of Complaints",
        barmode='stack'
    )
    graph = dcc.Graph(
        id='complaints-graph',
        figure=fig
    )
    return graph

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[  #outer div
    html.Div(children=[
        html.H1(children='Data Discovery'),
        html.H3(children='Finding Relationships Amongst Disparate Data Sets'),
        html.Div(children='By: Connor Watson, Priyanka Racharla, and Keval Kavle'),
        html.Div('''Data Source: https://opendata.cityofnewyork.us/'''),
        html.Br(),
           
        html.Div(children='''
        In this application we seek to find relationships amongst data sets
        which seemingly have no relationship. Thanks to recent efforts, we have
        access to lots of New York City data, and we intend to use data-driven story
        telling to inform the user of trends that exist in the data, while allowing
        for discovery of possibly new trends.
        ''', style={'text-align':'left'}),
        html.Br(),

        html.Div(children='''
        The growth of the human population has been increasing as time
        goes on. In conjunction with the Internet boom, NYC has become more of a hub
        for both jobs and technology. With the increase in population comes
        an increase in effect on the environment as well. People joke about
        the 'dirty Hudson River', but in actuality, the condition of NYC and
        our Earth is no joke.
        ''', style={'text-align':'left'}),
        html.Br(),
        
        html.Div(children='''
        Within our findings, we can see that NYC's population has very clearly
        been increasing. Using the tool below, you can discover this trend
        yourself. It may also be interesting to compare the constant increase
        in population with the trends in other attributes of our data set
        as well.
        ''', style={'text-align':'left'}),
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
        ''', style={'text-align':'left'}),
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
        ), #end dropdown 'dropdown-options'
        
        html.Div(id='graph-1'), #standardized data

        html.Br(),
        
        html.Div('''Figure 1 : Overall trends of multiple data columns throughout time.''', style={'text-align':'left'}),
        html.Div('''
        Note: This graph is NOT to scale. All data points have been standardized
        to fall in the range [0,1]. This graph allows you to see the overall trends across
        many years.''', style={'text-align':'left'}),
        html.Br(),
        html.Br(),
        html.Div('''----''', style={'text-align':'center'}),
        html.Br(),
        html.Br(),
        
        html.Div('''
        For a more accurate view, you may want to understand the data in it's most natural form.
        In contrast to the plot above, you can select two columns and see their relationship to
        each other. 
        ''', style={'text-align':'left'}),
        
        html.Div(id='graph-2'), #selectx vs selecty
        html.Br(),
        
        html.Div(id='graph-2-caption', style={'text-align':'left'}),

        html.Div(id='min-year', style={'display':'none'}),
        html.Div(id='max-year', style={'display':'none'}),
    
        html.Div(
            html.Div(
                dcc.RangeSlider(
                    id='year-slider',
                    min=1979, max=2018, step=1,
                    value=[1979,2018],
                    marks={y:str(y) for y in range(1979,2020,5)}
                ),
                style={'width': '600px', 'display': 'inline-block'}
            ),
            style={'text-align': 'center'}
        ), #end outer div containing RangeSlider
        
        html.Br(),
        
        html.Div(id='dropdowns', children=[
            html.Div(
                dcc.Dropdown(
                    id='select-x',
                    options=drop_options,
                    value='new_york_city_population',
                    multi=False
                ), #end dropdown 'select-x'
                className='six columns'
            ),
            html.Div(
                dcc.Dropdown(
                    id='select-y',
                    options=drop_options,
                    value='nyc_consumption_million_gallons_per_day',
                    multi=False
                ), #end dropdown 'select-y'
                className='six columns'
            )            
        ], className='row'),
        
        html.Br(),
        
        html.Div(id='graph-3-4', className='row'), #selectx and selecty
        html.Div(id='graph-34-caption', style={'text-align': 'left'}),
        html.Br(),
        
        html.Div(id='graph-5'), #Heatmap Corr between selectx/selecty
        html.Div(id='graph-5-caption', style={'text-align': 'left'}),
        html.Br(),
        html.Br(),
        html.Div('''----''', style={'text-align':'center'}),
        html.Br(),
        html.Br(),
        

        html.Div('''
        It's interesting to see through out time, how different variables correlate.
        Perhaps there are many more unknowns for us to discover. Perhaps, temporal
        trends aren't the only factors on environmental change. Yes, we can see that
        increasing population generally plays an impact on the other variables, which
        in turn impacts our environment. But, can location data point to changes as well?
        ''', style={'text-align': 'left'}),
        html.Br(),

        html.Div('''
        
        ''', style={'text-align': 'left'}),
        html.Br(),
        
        dcc.Dropdown(
            id='pri-year-selector',
            options=[{'label':str(y), 'value':y} for y in range(2010,2020)],
            value=2019,
            multi=False
        ), #select year for graph-6
        
        html.Div(id='graph-6'), #Priyanka Graph
        html.Div(id='graph-6-caption', style={'text-align': 'left'}),
        html.Br(),

        html.Div('''
        As you can see in the above chart, throughout each year, you can compare the amount
        of indoor complaints for each borough. After messing around with the data sets, you
        should notice that the bright red color stands out the most. That's because this
        represents the number of complaints for indoor air quality. So relatively, although
        each borough has a different population and a different set of residents, it's easy
        to understand why this color makes sense.
        ''', style={'text-align': 'left'}),
        html.Br(),

        html.Div('''
        If you've ever been to New York City, or visited any of the residential buildings,
        you would see on average that each building has awful indoor quality. Many people
        can relate to being inside one of these buildings and feeling grimy, humid, breathing
        in chemicals of the New York City air; this data makes sense, and speaks to the
        changing environment. If all of the boroughs have poor indoor air quality, then the
        outside air must be just as bad if not worse.
        ''', style={'text-align': 'left'}),
        html.Br(),
        html.Br(),
        html.Div('''----''', style={'text-align':'center'}),
        html.Br(),
        html.Br(),
        
        html.Div('''
        As shown, both time and space are contributing factors pointing to how the climate is
        changing. As the population of NYC increases, some factors like the amount of garbage
        collected or the amount of heating/cooling used per year increases as well. There seems
        to be some hope in recent years, as it seems like the data shows a more consious
        mindset towards water usage and compound production. But at the same time, per location,
        the air quality still is the highest contributor to complaints in the five boroughs,
        so are things really getting better? Looking at the data, what do you think will happen
        as the years go by, and is NYC really doing a good job of helping to save our planet?
        ''', style={'text-align': 'left'})
        
    ], style={'width': '1000px', 'display': 'inline-block'}) #end second outer div
], style={'text-align': 'center'} )#end outer div

@app.callback(
    Output('graph-1', 'children'),
    [Input('dropdown-options', 'value')],
)
def update_options(options_selected):
    #options_selected is the list of dropdown options
    my_graph = make_graph('yearly-data', options_selected, stan_df, 'Yearly Data')
    return my_graph
"""
@app.callback(
    Output('graph-2', 'children'),
    [Input('year-slider', 'value')])
def update_years_output(value):
    return 'You have selected "{}"'.format(value)
"""
@app.callback(
    [Output('min-year', 'children'),
     Output('max-year', 'children'),
     Output('graph-2', 'children'),
     Output('graph-3-4', 'children'),
     Output('graph-5', 'children'),
     Output('graph-2-caption', 'children'),
     Output('graph-34-caption', 'children'),
     Output('graph-5-caption', 'children')],
    [Input('select-x', 'value'),
     Input('select-y', 'value'),
     Input('year-slider', 'value')]
    )
def update_graph_2_3_4(x, y, year_range):
    temp_df = num_df[(num_df[x].notnull()) & (num_df[y].notnull())][['year',x,y]]
    temp_df2 = temp_df.loc[(temp_df['year'].isin(range(int(year_range[0]), int(year_range[1]))))]
    years = sorted(temp_df['year'].values)
    year0, year1 = str(years[0]), str(years[-1])
    titl = '{} vs {}'.format(x, y)
    my_graph2 = make_scatter('year-by-year-data', x, y, temp_df2, titl)
    #my_graph = 'you have selected: {}'.format(year_range)
    my_graph3 = make_scatter('year-by-x-data', 'year', x, temp_df2, x, mode='line')
    my_graph4 = make_scatter('year-by-y-data', 'year', y, temp_df2, y, mode='line')
    graphs_lst = [
                    html.Div(children=[my_graph3],
                        className='six columns'
                    ),
                    html.Div(children=[my_graph4],
                        className='six columns'
                    )
    ]

    corr_df = temp_df[[x, y]].corr()
    corr_plot = make_heatmap('heatmap-1', corr_df, [x,y], [x,y], 'Heatmap Correlation')

    g2_caption = '''
    Figure 2 : Plot of '{}' vs '{}', showing the actual data points as they relate to each
    other over time from {} to {}.
    '''.format(x, y, year_range[0], year_range[-1])

    g34_caption = '''
    Figure 3 (left) : '{}', Figure 4 (Right) : '{}', showing the actual data points over time from {} to {}.
    '''.format(x, y, year_range[0], year_range[-1])

    g5_caption = '''Figure 5 : Heatmap showing Pearson correlation between {} and {}'''.format(x, y)
    
    return year0, year1, my_graph2, graphs_lst, corr_plot, g2_caption, g34_caption, g5_caption

@app.callback(
    [Output('graph-6', 'children'),
     Output('graph-6-caption', 'children')],
    [Input('pri-year-selector', 'value')]
)
def functionName(year):
    environYr = final_environComplaint[final_environComplaint['Date_Received'].dt.year == year]

    complaintType = ['Asbestos', 'Indoor Air Quality', 'Mold','Asbestos/Garbage Nuisance', 'Indoor Sewage','Cooling Tower', 'Lead']
    numComplaints = [[],[],[],[],[],[],[]]
    
    for boro in borolist:
        boroYr = environYr[environYr['Incident_Address_Borough']==boro]
        complaintDF = boroYr.groupby('Complaint_Type_311').size()
        complaintIndex = 0
        for t in complaintType:
            try: 
                typeNum = complaintDF.loc[t]
                (numComplaints[complaintIndex]).append(typeNum)
            except: 
                (numComplaints[complaintIndex]).append(0)
            complaintIndex += 1

    g6_caption = '''Figure 6 : Different types of environmental complaints during {}.'''.format(year)

    stacked_bars = make_stacked_bars(environYr, year, complaintType, numComplaints)
    return stacked_bars, g6_caption


def main():
    #for opt in drop_options:
    #    print(opt)
    pass
    
if __name__ == '__main__':
    main()
    app.run_server(debug=True)
