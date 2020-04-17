import pandas as pd
import plotly.offline as offline
from plotly.offline import plot
from pathlib import Path
import functions as f
import matplotlib.pyplot as plt
from pandasql import *   

class DatabaseManipulator:
    __filePath = "Datasets/Iteratia6.csv"
    __df = pd.DataFrame()

    def __init__(self, base_path):
        self.__df = pd.read_csv(base_path / self.__filePath)

    @staticmethod
    def getCountryData(database,countryname):
        q = 'SELECT * FROM database WHERE country LIKE '+"'"+countryname+"'"
        x=sqldf(q, locals())
        return x


    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self,otherdf):
        self.__df=otherdf

if __name__ == '__main__':
    countryname="Romania"
    base_path = Path(__file__).parent
    d = DatabaseManipulator(base_path)
    d.df=DatabaseManipulator.getCountryData(d.df,countryname)
    figure=d.df.plot(kind='line',x='dt',y='AverageTemperature',marker='o')
    figure.set(title = "Average Temperature Over Time",
       xlabel = "Year",
       ylabel = "Temperature")
    figure.spines['top'].set_visible(False)
    figure.spines['right'].set_visible(False)
    figure.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

    plt.show()