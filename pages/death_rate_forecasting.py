import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from ml_model import get_forecasts_ml

dash.register_page(__name__)

countries_list = ['Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra',
       'Angola', 'Anguilla', 'Antigua and Barbuda', 'Argentina',
       'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
       'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
       'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan',
       'Bolivia (Plurinational State of)',
       'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina',
       'Botswana', 'Brazil', 'British Virgin Islands',
       'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi',
       'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands',
       'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
       'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', 'Côte d’Ivoire',
       'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czechia',
       "Democratic People's Republic of Korea",
       'Democratic Republic of the Congo', 'Denmark', 'Djibouti',
       'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt',
       'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
       'Eswatini', 'Ethiopia', 'Falkland Islands (Malvinas)',
       'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana',
       'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany',
       'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada',
       'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea',
       'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras',
       'Hungary', 'Iceland', 'India', 'Indonesia',
       'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Isle of Man',
       'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan',
       'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo[1]', 'Kuwait',
       'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia',
       'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein',
       'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia',
       'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
       'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
       'Micronesia (Federated States of)', 'Monaco', 'Mongolia',
       'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar',
       'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia',
       'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue',
       'North Macedonia',
       'Northern Mariana Islands (Commonwealth of the)', 'Norway',
       'occupied Palestinian territory, including east Jerusalem', 'Oman',
       'Other', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea',
       'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland',
       'Portugal', 'Puerto Rico', 'Qatar', 'Republic of Korea',
       'Republic of Moldova', 'Réunion', 'Romania', 'Russian Federation',
       'Rwanda', 'Saint Barthélemy', 'Saint Helena',
       'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin',
       'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
       'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia',
       'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore',
       'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands',
       'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka',
       'Sudan', 'Suriname', 'Sweden', 'Switzerland',
       'Syrian Arab Republic', 'Tajikistan', 'Thailand',
       'The United Kingdom', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga',
       'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
       'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine',
       'United Arab Emirates', 'United Republic of Tanzania',
       'United States of America', 'United States Virgin Islands',
       'Uruguay', 'Uzbekistan', 'Vanuatu',
       'Venezuela (Bolivarian Republic of)', 'Viet Nam',
       'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']


model_desc = html.Div([
    html.H2('Machine Learning Model Description'),
    html.P('The machine learning model used in this app is a Random Forest model, a popular ensemble learning method that uses decision trees to build a predictive model.'),
    html.P('The model is trained on a dataset containing COVID deaths data for various countries, with the following features:'),
    html.Ul([
        html.Li('dayoftheyear: the day of the year (1-365)'),
        html.Li('week: the week number (1-52)'),
        html.Li('season: the season (1=Winter, 2=Spring, 3=Summer, 4=Fall)'),
        html.Li('month: the month (1-12)'),
        html.Li('ndeaths_lag1: the number of deaths on the previous day'),
        html.Li('ndeaths_lag7: the number of deaths 7 days ago'),
        html.Li('ndeaths_lag14: the number of deaths 14 days ago'),
        html.Li('ndeaths_lag30: the number of deaths 30 days ago'),
        html.Li('ndeaths_mean7: the mean number of deaths over the past 7 days'),
        html.Li('ndeaths_mean30: the mean number of deaths over the past 30 days'),
        html.Li('ndeaths_mean14: the mean number of deaths over the past 14 days')
    ]),
    html.P('Given a set of these features for a particular country, the model predicts the number of COVID deaths for the next day.'),
    html.P('The Random Forest model is chosen because it is well-suited for datasets with many features and a large number of samples, and tends to produce accurate predictions. It works by training multiple decision trees on different subsets of the data and combining their predictions to reduce overfitting and improve generalization performance.'),
    html.P('In this app, the model\'s performance is evaluated using various metrics such as Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) and the results are displayed alongside the forecasted data for the selected country.')
])

layout = html.Div([

    dbc.Row([
        dbc.Col( [
            dbc.Row([
                dbc.Col(html.H1('COVID Deaths Forecasting for Countries'), className='mt-3')
             ]),
            dbc.Row([
                dbc.Col( model_desc, className='mt-3')
            ]),
        ] , width = 4),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Label('Select a country'),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[
                            {'label': c, 'value': c} for c in countries_list
                        ],
                        value='India'
                    )
                ], width=6)
            ], className='mt-3'),
            dbc.Row([
                dbc.Col(dcc.Loading(dcc.Graph(id='forecast-graph'), width=12))
            ], className='mt-3')
        ],width = 8),
    ])

    
    
])

@callback(Output('forecast-graph', 'figure'), [Input('country-dropdown', 'value')])
def update_graph(country):
    # code to get the forecast data and model performance for the selected country
    # create a plotly graph object with the data
    fig = get_forecasts_ml(country)
    return fig