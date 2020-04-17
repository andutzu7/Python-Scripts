from fbprophet import Prophet
import pandas as pd
from fbprophet.plot import plot_plotly
import plotly.offline as py
from plotly.offline import plot
from pathlib import Path
import matplotlib.pyplot as plt
from pandasql import *
import datetime

def getCountryData(database, countryname):
    q = 'SELECT * FROM database WHERE country LIKE ' + "'" + countryname + "' AND ds<2000"
    x = sqldf(q, locals())
    return x


df = pd.read_csv('Iteratia6.csv')
m = Prophet()
countryName="Romania" 
countrydf=getCountryData(df,countryName)
for index, row in countrydf.iterrows():
    countrydf.loc[index, 'ds'] = datetime.datetime(int(row['ds']), 1, 1)
print(countrydf)
m.fit(countrydf)
future = m.make_future_dataframe(periods=12,freq='Y')

future.tail()
forecast = m.predict(future)

fig = plot_plotly(m, forecast)  # This returns a plotly Figure
py.plot(fig)