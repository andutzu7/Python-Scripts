
import pandas as pd
  
import plotly.offline as offline

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from pathlib import Path

import functions as f
#constants i didnt include in the GUI
base_path = Path(__file__).parent
df_init = pd.read_csv(base_path/"wordT.csv") #datasetul + o incercare de universal path
howMany=10 #cate trepte sa aiba sliderul
yStep=10 #din cat in cat se incrementeaza
firstYear=f.getFirstYearOfDataframe(df_init) #i could also get the first year of the dataset
carbonIncreasedPercent=0.2#a self explanatory constant
#####################################
years=f.generateYears(howMany,yStep,firstYear) #anii pe care ii vrem pt predictie
#modelam pt nevoile noastre dataframeul
df_init = f.updateDatasetYears(df_init,years,carbonIncreasedPercent)

df_init = f.updateDatasetIsoCode(df_init)
print(df_init)
#this is a list the maps at different time periods

data_slider = []

data_slider=f.separatePerYearMaps(df_init,data_slider)
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

