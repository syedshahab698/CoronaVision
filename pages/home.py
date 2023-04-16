import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.P(
            "Please select one of the following pages to continue:"
        ),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("COVID-19 Dashboard", className="card-title"),
                                html.P("View interactive charts and maps of COVID-19 cases and deaths."),
                                dbc.Button("Go to Dashboard", color="primary", href="/eda-report"),
                            ]
                        )
                    )
                )
            , width=6, className="mb-4"),
            dbc.Col(
                html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("COVID Death Forecasts", className="card-title"),
                                html.P("View and compare machine learning model forecasts of COVID-19 deaths for selected countries."),
                                dbc.Button("Go to Forecasts", color="primary", href="/death-rate-forecasting"),
                            ]
                        )
                    )
                )
            , width=6, className="mb-4")
        ]),

])