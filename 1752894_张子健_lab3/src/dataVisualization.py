import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = pd.read_csv('BlackFriday.csv')
buyer_1 = data[(data['Product_Category_1']==1) | (data['Product_Category_2']==1) | (data['Product_Category_3']==1)]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
diagrame_1_purpose = '''The following diagrame aims to illustrate **general purchase value** of the three different cities

This is done by comparing the average purchase value of the **same occupations** among **different cities**

As wo can see, city C is somehow ***richer*** than the other two. However, city A's occupation 8 is really abnormal.
'''
diagrame_2_purpose = '''The following diagrame aims to illustrate the relationship between **product category** and the **buyers' attribute**.

You can select the category of product that you are intersted by the Dropown menu below.
'''
app.layout = html.Div([
    html.H1('Two analyses based on BlackFriday dataset'),
    html.H2('Which city buys more?'),
    dcc.Markdown(diagrame_1_purpose),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x = np.arange(0,21),
                    y = data[data['City_Category']==i][['Occupation','Purchase']].groupby('Occupation').mean()['Purchase'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in data.City_Category.unique()
            ],
            'layout': go.Layout(
                xaxis={'title': 'Occupation'},
                yaxis={'title': 'Purchase value'},
                margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    html.H2('Who are buying this?'),
    dcc.Markdown(diagrame_2_purpose),
    dcc.Dropdown(
        id = 'category',
        options=[
            {'label': '1', 'value': 1},
            {'label': '2', 'value': 2},
            {'label': '3', 'value': 3},
            {'label': '4', 'value': 4},
            {'label': '5', 'value': 5},
            {'label': '6', 'value': 6},
            {'label': '7', 'value': 7},
            {'label': '8', 'value': 8},
            {'label': '9', 'value': 9},
            {'label': '10', 'value': 10},
            {'label': '11', 'value': 11},
            {'label': '12', 'value': 12},
            {'label': '13', 'value': 13},
            {'label': '14', 'value': 14},
            {'label': '15', 'value': 15},
            {'label': '16', 'value': 16},
            {'label': '17', 'value': 17},
            {'label': '18', 'value': 18},
        ],
        value=1, 
    ),
    html.Div([
    dcc.Graph(
        id = 'occupation',
        
        style={'height': 400},
    ),
    dcc.Graph(
        id = 'age',
        
        style={'height': 400},
    ),
    html.Div([
    dcc.Graph(
        id = 'gender',
        
        style={'height': 400},
    ),
    dcc.Graph(
        id = 'city',
        
        style={'height': 400},
    )],
        style={'columnCount': 1},
    )
    ],style={'columnCount': 4})

])
@app.callback(
    [Output('age','figure'),
     Output('occupation','figure'),
     Output('gender','figure'),
     Output('city','figure'),],
     [Input('category', 'value')]
)
def update_diagrams(cate):
    buyer = buyer_1 = data[(data['Product_Category_1']==cate) | (data['Product_Category_2']==cate) | (data['Product_Category_3']==cate)] 
    return ({
        'data':[
            go.Scatter(
                x=buyer.groupby('Age').count().index,
                y=buyer.groupby('Age').count()['User_ID'],
                name='User number in the age range',

            ),
        ],
        'layout':go.Layout(
            title='Age',
            showlegend=True,
            margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
        )
    },
    {
        'data':[
            go.Bar(
                x=buyer.groupby('Occupation').count().index,
                y=buyer.groupby('Occupation').count()['User_ID'],
                name='User number of the occupation',

            ),
        ],
        'layout':go.Layout(
            title='Occupation',
            showlegend=True,
            margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
        )
    },
    {
        'data':[
            go.Pie(
                labels=buyer.groupby('Gender').count().index,
                values=buyer.groupby('Gender').count()['User_ID'],
                name='User number of the Gender',

            ),
        ],
        'layout':go.Layout(
            title='Gender',
            showlegend=True,
            margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
        )
    },
    {
        'data':[
            go.Pie(
                labels=buyer.groupby('City_Category').count().index,
                values=buyer.groupby('City_Category').count()['User_ID'],
                name='User number of the City_Category',

            ),
        ],
        'layout':go.Layout(
            title='City_Category',
            showlegend=True,
            margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
            legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
        )
    })





if __name__ == '__main__':
    app.run_server(debug=True)