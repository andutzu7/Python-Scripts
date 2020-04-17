import numpy as np
import pandas as pd
import re
import math
import DateTime
from pandasql import *
import pycountry

def calculateTemperatures(sign, percent, baseTemperature, noYears):
    carbonEmissionPrincipal = 391  # data extracted from another database i didnt link here
    procent = percent * noYears
    if (sign == 0):
        newCarbonEmission = carbonEmissionPrincipal - (percent * carbonEmissionPrincipal)
    else:
        newCarbonEmission = carbonEmissionPrincipal + (percent * carbonEmissionPrincipal)

    raport = newCarbonEmission / carbonEmissionPrincipal
    deltaTemperature = np.log(raport)
    deltaTemperature = deltaTemperature * 1.66
    result = baseTemperature + deltaTemperature
    return result


# This function returs a list of evenly spaced years for the slider scale
def generateYears(howMany, yStep, firstYear):
    years = []
    for i in range(0, howMany):
        year = firstYear + i * yStep
        years.append(year)
    return years

def getYears(dataframe):
    years = []
    for year in dataframe.dt.unique():
        years.append(year)
    return years
# This returns the first year value of a given dataframe
def getFirstYearOfDataframe(df):
    return df['Year'].values[0]


def updateDatasetYears(data):
    dictionariesList = []  # list to store the rows
    for copy in data.iterrows():  # selecting a row
        separator = DateTime.DateFunctions.get_separator(copy[1][0])
        tokens = copy[1][0].split(separator)
        var = DateTime.DateFunctions.extract_year(tokens)
        copy[1][0] = var
        copyFrame = {'dt': copy[1][0], 'AverageTemperature': copy[1][1],
                     'AverageTemperatureUncertainty': copy[1][2],
                     'Country': copy[1][3]}  # creating a new row for the dataFrame
        dictionariesList.append(copyFrame)
    data = pd.DataFrame(dictionariesList, columns=['dt', 'AverageTemperature',
                                                   'AverageTemperatureUncertainty',
                                                   'Country'])  # replacing the values in the dataframe with the newly updated ones
    return data


# This function is used to add a new column in a given dataframe,converting the countryname into a ISO abbreviation
def updateDatasetIsoCode(data):
    input_countries = data['Country']
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
    codes = [countries.get(country, 'Unknown code') for country in input_countries]
    data['iso_code'] = codes
    return data


# this function takes as input the dataframe an slices it by years, mapping the result into a
# dictionary that will be stored into a data_slider, to be displayed later
def separatePerYearMaps(df_init, data_slider):
    for year in df_init.dt.unique():
        df = df_init[df_init['dt'] == year]

        for col in df.columns:  # converting columns into strings so i can add any text i want
            df[col] = df[col].astype(str)
        df['text'] = df['Country']  # hover text
        ### create the dictionary with the data for the current year
        data_one_year = dict(
            type='choropleth',
            autocolorscale=False,
            locations=df['iso_code'],  # what to display, only taking iso codes to access the builtin map
            z=df['AverageTemperature'],  # z component gives the scale values
            text=df['text'],
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorscale='Blues',
            colorbar=dict(
                title="World Temperature Evolution")
        )
        data_slider.append(data_one_year)  # I add the dictionary to the list of dictionaries for the slider
    return data_slider;


# this function generates the map steps used in the slider
# by creating for every avaliable map a "slider-step",which is a dictionary
def generateMapSteps(data_slider, years, steps, firstYear, yStep):
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)],
                    # we make all the other steps false to they wont overlap and display their individual data
                    label='Year {}'.format(i * yStep + firstYear))  # labeling the slider according to our dataset
        step['args'][1][i] = True  # we make the current step true so only its data will be shown on hovering/colors
        steps.append(step)
    return steps

#i hate this function but it gets the job done
def generate_avg_dataframe(database,minyear):
    dictionariesList = []
    index=0.0
    value=0.0
    lastYear=minyear
    rowindex=0
    for copy in database.iterrows():  # selecting a row
        rowindex=rowindex+1
        print(rowindex)
        year=copy[1][1]
        if year>=minyear:
            if lastYear==year and math.isnan(year)==False:
                index=index+1
                value=value+copy[1][2]
            else:
                if index>0:
                    copyFrame = {'dt': int(lastYear), 'AverageTemperature': value/index,
                         'AverageTemperatureUncertainty': copy[1][3],
                        'Country': copy[1][4]}  # creating a new row for the dataFrame
                    dictionariesList.append(copyFrame)
                    index=0
                    value=0
        lastYear=year
    data = pd.DataFrame(dictionariesList, columns=['dt', 'AverageTemperature',
                                                   'AverageTemperatureUncertainty',
                                                   'Country'])  # replacing the values in the dataframe with the newly updated ones
    return data
    

def getCountryData(database,countryname):
    q = 'SELECT * FROM database WHERE country LIKE '+"'"+countryname+"'"
    x=sqldf(q, locals())
    return x


"""
#o solutie groaznica
def generate_avg_dataframe(database):
    dictionariesList = []
    dfindex=0
    for country in database.Country.unique():
        index=0
        value=0
        prevYear=0
        for year in database.dt:
            if year >= 1900:
                dfindex=dfindex+1
                print ("dfindex is",dfindex)
                value=(value + database.at[dfindex,'AverageTemperature'])
                print (value)
                index=index+1
                if index>0:
                    copyFrame = {'dt': int(year), 'AverageTemperature': value/index,
                                         'AverageTemperatureUncertainty': 444,
                                         'Country': country}  # creating a new row for the dataFrame
                    print(copyFrame)
                    index=0
                    value=0
                    dictionariesList.append(copyFrame)
            
    data = pd.DataFrame(dictionariesList, columns=['dt', 'AverageTemperature',
                                                   'AverageTemperatureUncertainty',
                                                   'Country'])  # replacing the values in the dataframe with the newly updated ones
    print (data)
    return data
"""
"""

def generate_avg_dataframe(database,lowestYear):
    dictionariesList = []
    pysqldf = lambda q, database: sqldf(q, globals())
    index=0
    for country in database.Country.unique():
        for year in database.dt.unique():
            if int(year)>=lowestYear:
                print("Querying nr "+str(index))
                q = 'SELECT AVG(AverageTemperature) FROM database WHERE dt='+str(year)+' AND Country LIKE ' + "'" + country + "'"
                x = re.findall("[+-]?\d+\.\d+", str(sqldf(q, locals())))
                #x=str(sqldf(q,locals()))
                if not x:
                    val=-1
                else:
                    val=x[0]
                copyFrame = {'dt': int(year), 'AverageTemperature': val,
                             'AverageTemperatureUncertainty': 444,
                             'Country': country}  # creating a new row for the dataFrame
                dictionariesList.append(copyFrame)
                print(copyFrame)
                print("added entry nr "+str(index))
                index=index+1
    data = pd.DataFrame(dictionariesList, columns=['dt', 'AverageTemperature',
                                                   'AverageTemperatureUncertainty',
                                                   'Country'])  # replacing the values in the dataframe with the newly updated ones
    return data
"""