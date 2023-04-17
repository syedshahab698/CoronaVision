import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from prophet import Prophet
# from matplotlib import pyplot as plt
# Python
# from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objs as go

# Load the data
covid_data = pd.read_csv('COVID-19-global-data.csv')
covid_data.columns = covid_data.columns.str.strip().str.lower()

# Convert date column to datetime
covid_data['date_reported'] = pd.to_datetime(covid_data['date_reported'])

# Create new columns for week, month, and season
covid_data['day'] = covid_data['date_reported'].apply(lambda x: x.timetuple().tm_yday)
covid_data['week'] = covid_data['date_reported'].dt.week
covid_data['month'] = covid_data['date_reported'].dt.month
covid_data['season'] = (covid_data['month'] % 12 + 3) // 3

def get_forecasts_ml(country):
    global covid_data
    india_data = covid_data.loc[covid_data['country']==country,['date_reported', 'day','week', 'month', 'season', 'deaths'] ].copy()
    india_data = india_data.reset_index(drop=True)

    # # adding foreacsts from trend based model to as independent variable
    # india_data_fr = india_data[['date_reported', 'deaths']]
    # india_data_fr.columns = ['ds', 'y']
    # m = Prophet(growth = 'linear')
    # m.fit(india_data_fr)

    # forecast = m.predict(india_data_fr[['ds']])
    # forecast.loc[forecast['yhat']<0, 'yhat'] = 0

    # india_data['model_forecasts'] = forecast['yhat']

    #
    dates = india_data['date_reported']
    india_data = india_data.drop('date_reported', axis=1)


    india_data = india_data.loc[india_data['deaths']!=0]

    # adding lag variables
    india_data['lag_1'] = india_data['deaths'].shift(1)
    india_data['lag_7'] = india_data['deaths'].shift(7)
    india_data['lag_14'] = india_data['deaths'].shift(14)
    india_data['lag_30'] = india_data['deaths'].shift(30)

    # adding lag variables
    # Add weekly and monthly average variables
    india_data['weekly_avg'] = india_data['deaths'].rolling(window=7).mean().shift(1)
    india_data['monthly_avg'] = india_data['deaths'].rolling(window=30).mean().shift(1)

    india_data = india_data.dropna()


    # Define the independent and dependent variables
    X = india_data.drop('deaths', axis=1)
    y = india_data['deaths']


    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Create the regression model
    model = SVR()

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Evaluate the model
    r2 = r2_score(y_test, y_pred)
    print('R-squared:', r2)
    
    # add dates back
    X_test['date'] = dates
    X_train['date'] = dates
    X['date'] = dates
    
    trace_actual = go.Scatter(
        x=X['date'],
        y=y,
        name='Actual Deaths',
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(color='red', size=8)
    )
    
    trace_predicted = go.Scatter(
        x=X_test['date'],
        y=y_pred,
        name='Predicted Deaths',
        mode='lines',
        line=dict(color='blue', width=2)
    )
    
    # Create layout
    layout = go.Layout(
        title='COVID-19 Deaths Forecast - {}'.format(country),
        xaxis=dict(title='Date'),
        yaxis=dict(title='Number of Deaths')
    )
    
    # Add both traces to a data list
    fig_data = [trace_actual, trace_predicted]
    
    # Create the figure object
    fig = go.Figure(data=fig_data, layout=layout)
    fig.update_layout(plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3')
    return fig
            

def get_forecasts_fbprophet(country):
    global covid_data
    india_data = covid_data.loc[covid_data['country']==country,['date_reported', 'deaths'] ].copy()
    india_data = india_data.reset_index(drop=True)

    

    # Run fb prophet model
    india_data_fr = india_data[['date_reported', 'deaths']]
    india_data_fr.columns = ['ds', 'y']

    train_data, test_data = train_test_split(india_data_fr, test_size=0.2, shuffle=False)

    m = Prophet(growth = 'linear')
    m.fit(train_data)

    forecast = m.predict(test_data[['ds']])
    forecast.loc[forecast['yhat']<0, 'yhat'] = 0

    test_data = test_data.reset_index(drop=True)
    test_data['model_forecasts'] = forecast['yhat']

    trace_actual = go.Scatter(
        x=india_data_fr['ds'],
        y=india_data_fr['y'],
        name='Actual Deaths',
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(color='red', size=8)
    )
    
    trace_predicted = go.Scatter(
        x=test_data['ds'],
        y=test_data['model_forecasts'],
        name='Predicted Deaths',
        mode='lines',
        line=dict(color='blue', width=2)
    )
    print(test_data.head())
    
    # Create layout
    layout = go.Layout(
        title='COVID-19 Deaths Forecast - {}'.format(country),
        xaxis=dict(title='Date'),
        yaxis=dict(title='Number of Deaths')
    )
    
    # Add both traces to a data list
    fig_data = [trace_actual, trace_predicted]
    
    # Create the figure object
    fig = go.Figure(data=fig_data, layout=layout)
    fig.update_layout(plot_bgcolor='#F3F3F3', paper_bgcolor='#F3F3F3')
    return fig