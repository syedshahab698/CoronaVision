
## Installation

Install my-project with npm

```bash
  pip install -r requirements.txt
```

## Usage
To use this tool, run the app.py script:

```bash
  python app.py
```

This will start a web server that you can access in your web browser by navigating to http://localhost:8050. You can use this web interface to select a country and view its forecasted COVID-19 deaths over time.

## Machine Learning Model
The machine learning model used in this app is a Random Forest model, a popular ensemble learning method that uses decision trees to build a predictive model. It is trained on a dataset containing COVID deaths data for various countries.

## Time Series Forecasting Model
The time series forecasting model used in this app is the FB Prophet model, a time series forecasting model developed by Facebook. It is used to forecast future deaths based on historical COVID deaths data.

## Acknowledgements
This project was built using data from the Our World in Data COVID-19 deaths dataset. The machine learning model was built using scikit-learn, while the time series forecasting model was built using the FB Prophet library.

## License
This project is licensed under the MIT License.