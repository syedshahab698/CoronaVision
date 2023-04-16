import dash
from dash import html, dcc, callback, Input, Output
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from main import deaths_by_regions, top6_countries_confirmed_cases, view7, view8, view1, view3

dash.register_page(__name__)



# Create a list of Plotly chart objects to display in the carousel
# charts = []
# for i in range(5):
#     x = np.random.randn(100)
#     y = np.random.randn(100)
#     trace = go.Scatter(x=x, y=y, mode='markers')
#     chart = dcc.Graph(figure={'data': [trace]})
#     charts.append(chart)


charts = {
    "DashBoard" : view1(),
    "Region-wise Total Cases" : view3(),
   "COVID Daily Deaths: Top 4 Regions" : deaths_by_regions(),
   "Top 6 Countries by Confirmed Cases": top6_countries_confirmed_cases(),
   
    "COVID-19 Cases by Country and Region": view7(), 
    "Covid's Impact On Countries" : view8()

}

def two_charts_layout(x):
    a,b =x
    output = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            figure = a
                        )
                    )
                ),
                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            figure = b
                        )
                    )
                )
            ]
        )
    ],style = {'margin-top':'10px'}
    
)

    return output

def one_chart_layout(x):
    return html.Div([
        dcc.Graph(figure = x)
    ], style = {'margin-top':'10px'})

eda_figures = dbc.Tabs(
    [
        dbc.Tab(two_charts_layout(chr), label=name) if isinstance(chr,tuple) else dbc.Tab(one_chart_layout(chr), label=name)  for name, chr in charts.items()
    ]
)

layout = html.Div(children=[
	html.Br(),
    html.Div(eda_figures, style={'height': '500px'}),
])


# @callback(
#     Output(component_id='analytics-output', component_property='children'),
#     Input(component_id='analytics-input', component_property='value')
# )
# def update_city_selected(input_value):
#     return f'You selected: {input_value}'