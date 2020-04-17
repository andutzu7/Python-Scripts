import pandas as pd
import plotly.offline as offline
from plotly.offline import plot

from pathlib import Path
import functions as f


class DatabaseManipulator:
    __filePath = "Datasets/Iteratia6.csv"
    __df = pd.DataFrame()

    def __init__(self, base_path):
        self.__df = pd.read_csv(base_path / self.__filePath)

    @property
    def df(self):
        return self.__df


if __name__ == '__main__':
    base_path = Path(__file__).parent
    d = DatabaseManipulator(base_path)
    df_init = d.df
        
    #this is a list the maps at different time periods

    data_slider = []

    data_slider=f.separatePerYearMaps(df_init,data_slider)
    #getdb years
    
    years=[]
    years=f.getYears(df_init)
    firstYear=years[0]
    yStep=1
    #a list where we store all the year steps
    steps = []

    steps = f.generateMapSteps(data_slider,years,steps,firstYear,yStep)
        
    ##  I create the 'sliders' object from the 'steps' 

    sliders = [dict(active=0, steps=steps)]  

    # I set up the layout (including slider option)

    layout = dict(geo=dict(   showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
       ),
                  sliders=sliders)
       
    #Creez figura propriu zisa
    fig = dict( data=data_slider, layout=layout )
    #Plotez si afisez in browser rezultatul
    offline.plot(fig, auto_open=True)