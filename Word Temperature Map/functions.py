import pycountry
import numpy as np
import pandas as pd
from random import randrange
from pathlib import Path

#TODO: DE FACUT FORMULA PT TEMPERATURI ACCURATE

def calculateTemperatures(sign,percent,baseTemperature,noYears):
	carbonEmissionPrincipal=391 #data extracted from another database i didnt link here
	percent=percent*noYears
	if(sign==0):
		newCarbonEmission=carbonEmissionPrincipal-(percent*carbonEmissionPrincipal) 
	else:
		newCarbonEmission=carbonEmissionPrincipal+(percent*carbonEmissionPrincipal) 
	
	raport=newCarbonEmission/carbonEmissionPrincipal
	deltaTemperature=np.log(raport)
	deltaTemperature=deltaTemperature*1.66
	result =baseTemperature+deltaTemperature
	return result

#This function returs a list of evenly spaced years for the slider scale
def generateYears(howMany,yStep,firstYear):
	years = []
	for i in range(0,howMany):
		year = firstYear+i*yStep
		years.append(year)
	return years
#This returns the first year value of a given dataframe
def getFirstYearOfDataframe(df):
	return df['Year'].values[0]
#Parameters: data - a dataframe containing the data needed to be shown in a cronopleth
#Years: a list of years to be added in a final dataframe
#This function copies the current entries of the dataframe and adds the years in the given scale
#This function is uselful when you have a dataset that only contains data for one year and
#you want to transform it into a multi year database(updating the values with various functions)
def updateDatasetYears(data,years,carbonIncreasedPercent):
	dictionariesList = []#list to store the rows
	sign = 0 if carbonIncreasedPercent>0 else 1
	for year in years:
		yearsNo=year-years[0]
		for copy in data.iterrows(): #selecting a row
			#print(sign,carbonIncreasedPercent,copy[1][2],yearsNo) # FAULTY FUNCTION GOTTA SOLVE THAT
			copy[1][0]=year #hardcoded, has to be changed if the dataset isnt wordT.csv and in this case it selects the year
			#copy[1][2]=calculateTemperatures(sign,carbonIncreasedPercent,copy[1][2],yearsNo) #updating the temperature colun
			copy[1][2]=copy[1][2]+randrange(100)
			copyFrame={'Year': copy[1][0],'Country' : copy[1][1],'Temperature':copy[1][2]}#creating a new row for the dataFrame
			dictionariesList.append(copyFrame)
	data =  pd.DataFrame(dictionariesList,columns=['Year', 'Country', 'Temperature',])#replacing the values in the dataframe with the newly updated ones
	return data
#This function is used to add a new column in a given dataframe,converting the countryname into a ISO abbreviation
def updateDatasetIsoCode(data):
	input_countries=data['Country']
	countries = {}
	for country in pycountry.countries:
		countries[country.name] = country.alpha_3
	codes = [countries.get(country, 'Unknown code') for country in input_countries]
	data['iso_code']=codes
	return data
#this function takes as input the dataframe an slices it by years, mapping the result into a 
#dictionary that will be stored into a data_slider, to be displayed later
def separatePerYearMaps(df_init,data_slider):
	for year in df_init.Year.unique():
		df = df_init[df_init['Year']==year]

		for col in df.columns: #converting columns into strings so i can add any text i want
			df[col] = df[col].astype(str)
		df['text'] = df['Country'] # hover text
    	### create the dictionary with the data for the current year	
		data_one_year = dict(
			type='choropleth',
			autocolorscale=False,
			locations=df['iso_code'],#what to display, only taking iso codes to access the builtin map
			z=df['Temperature'],#z component gives the scale values
			text=df['text'],
			marker_line_color='darkgray',
			marker_line_width=0.5,
			colorscale='YlGn',
			colorbar=dict(
					title="World Temperature Evolution")
						)
		data_slider.append(data_one_year)# I add the dictionary to the list of dictionaries for the slider
	return data_slider;
#this function generates the map steps used in the slider
#by creating for every avaliable map a "slider-step",which is a dictionary
def generateMapSteps(data_slider,years,steps,firstYear,yStep):
	for i in range(len(data_slider)):
		step = dict(method='restyle',
	                args=['visible', [False] * len(data_slider)],#we make all the other steps false to they wont overlap and display their individual data
	                label='Year {}'.format(i*yStep + firstYear))#labeling the slider according to our dataset   
		step['args'][1][i] = True #we make the current step true so only its data will be shown on hovering/colors
		steps.append(step)
	return steps