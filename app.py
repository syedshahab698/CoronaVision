from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Define your pages here
pages = [
    {"name": "Home", "path": "/", "relative_path": "/"},
    {"name": "Covid Report", "path": "/eda-report", "relative_path": "/eda-report"},
    {"name": "Covid Death Forecasting", "path": "/death-rate-forecasting", "relative_path": "/death-rate-forecasting"},
]

app.layout = html.Div([
	
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
            for page in pages
        ],
        brand="CoronaVision",
        brand_href="#",
        sticky="top",
        color="dark",
        dark=True
    ),

    html.Div([
        html.Div(
        [
            html.H1("COVID Insights and Forecaster!", className="display-3"),
            html.P(
                "Tracking the Pandemic Worldwide.",
                className="lead"
            ),
            html.Hr(className="my-2"),
            html.P(
                "Explore the latest COVID-19 data and trends with our interactive dashboard. With accurate forecasts and data visualizations, our app provides you with valuable insights into the pandemic"
            ),
           
        ],
        
        
    ),
 

    # html.Div(
    #     [
    #         html.Div(
    #             dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"]
    #             )
    #         )
    #         for page in dash.page_registry.values()
    #     ]
    # ),

	dash.page_container

    ], style = {'margin-left':'10%', 'margin-right':'10%'})
    
], style={'background-color': '#F8F9FA', })

if __name__ == '__main__':
	app.run_server(debug=False)