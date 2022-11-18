'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
from time import strptime
from multiprocessing.sharedctypes import Value
import json

date_format = "%Y-%m-%d"

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def Get_Info(symbol, chart_type, time_series, start_date, end_date):
    keystring = ""
    url = ""
    if time_series[0] == "1":
        url = 'https://www.alphavantage.co/query?function=' + "TIME_SERIES_INTRADAY" + '&symbol=' + symbol[0] + '&interval=60min&apikey=4NJ262WL2WQKBMQ1'
        keystring = "Time Series (60min)"
    elif time_series[0] == "2":
        url = 'https://www.alphavantage.co/query?function=' + "TIME_SERIES_DAILY_ADJUSTED" + '&symbol=' + symbol[0] + '&outputsize=full&apikey=4NJ262WL2WQKBMQ1'
        keystring = "Time Series (Daily)"
    elif time_series[0] == "3":
        url = 'https://www.alphavantage.co/query?function=' + "TIME_SERIES_WEEKLY" + '&symbol=' + symbol[0] + '&apikey=4NJ262WL2WQKBMQ1'
        keystring = "Weekly Time Series"
    elif time_series[0] == "4":
        url = 'https://www.alphavantage.co/query?function=' + "TIME_SERIES_MONTHLY" + '&symbol=' + symbol[0] + '&apikey=4NJ262WL2WQKBMQ1'
        keystring = "Monthly Time Series"
    # Return information from url
    r = requests.get(url)
    data = r.json()
    x_axis_values = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []
    # Iterate through dictionary, populate lists for each attribute
    for value in data[keystring]:
        if(convert_date(value[0:10]) >= start_date and convert_date(value[0:10]) <= end_date):
            x_axis_values.append(value)
            open_values.append(float(data[keystring][value]['1. open']))
            high_values.append(float(data[keystring][value]['2. high']))
            low_values.append(float(data[keystring][value]['3. low']))
            close_values.append(float(data[keystring][value]['4. close']))
    # Bar Graph
    api_chart = ""
    if chart_type[0] == "1":
        api_chart = pygal.Bar()
        api_chart.title = "Stock data for " + symbol[0] + ": " + start_date.strftime(date_format) + " - " + end_date.strftime(date_format)
        api_chart.x_labels = x_axis_values
    # Line Graph
    if chart_type[0] == "2":
        api_chart = pygal.Line()
        api_chart.title = "Stock data for " + symbol[0] + ": " + start_date.strftime(date_format) + " - " + end_date.strftime(date_format)
        api_chart.x_labels = x_axis_values
            
    api_chart.add("Open", open_values)
    api_chart.add("High", high_values)
    api_chart.add("Low", low_values)
    api_chart.add("Close", close_values)
    # Return the chart to routes.py
    return api_chart.render_data_uri()