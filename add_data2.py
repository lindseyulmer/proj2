O"""This module creates a base data set that add_data() build on.
add_data(startdata,newdatafile,startdatastate, newdatastate, states, newfilename)
The purpose of this module is to prepare data for visualization
"""
#Import Packages
import pandas as pd
import geopandas as gpd
# Read the coviddata from a csv into a dataframe
coviddata = pd.read_csv('../data/raw_2_covid_latest.csv', index_col=0)
# Read in shapefile and examine data
contiguous_usa = gpd.read_file('../shapefiles/cb_2018_us_state_20m.shp')
# Merge shapefile with population data
case_states = contiguous_usa.merge(coviddata, left_on = 'NAME', right_on='State/Territory')
# Drop Alaska and Hawaii
case_states = case_states.loc[~case_states['NAME'].isin(['Alaska', 'Hawaii',"Puerto Rico"])]
case_states.to_csv('basedata.csv')
case_states.head()
#Define all states
allstates=["Maryland", "Iowa", "Delaware", "Ohio", "Pennsylvania", "Nebraska", "Washington",
	 "Alabama", "Arkansas", "New Mexico", "Texas", "California", "Kentucky", "Georgia", "Wisconsin",
	 "Oregon", "Missouri", "Virginia", "Tennessee", "Louisiana", "New York", "Michigan", "Idaho",
	 "Florida","Illinois", "Montana", "Minnesota", "Indiana","Massachusetts","Kansas","Nevada",
	 "Vermont", "Connecticut","New Jersey","District of Columbia","North Carolina","Utah","North Dakota",
         "South Carolina","Mississippi","Colorado","South Dakota","Oklahoma","Wyoming","West Virginia",
         "Maine","New Hampshire","Arizona","Rhode Island"]
#Define key states
key=["Arizona", "Florida", "Georgia", "Michigan", "Minnesota", "North Carolina", "Ohio",
         "Pennsylvania", "Texas", "Wisconsin"]
def add_data(startdata,newdatafile,startdatastate, newdatastate, states, newfilename):
    """
    Args:
        startdata (str):filename with path of starting dataframe that includes geopandas
	shape information, recommended use basedata.csv from github repo
        newdatafile (str): filename with path to csv of new data to be added
        startdatastate(str): name of state column of starting data
        newdatastate(str): name of state column of new data
        column (str): column from new data file to be added, only add one at a time,
	rerun function to add more than one colummn
        states(list): list of strings of the desired states
        newfilename(str):name of new data file generated
    Returns:
	newfilename: the dataframe with the newly added data as a csv"""
    # Read the dataframe to add too
    basedata = pd.read_csv(startdata, index_col=0)
    #Read data being added as a dataframe
    newdf=pd.read_csv(newdatafile)
    #Find all non-desired states
    dropstates=[]
    for eachstate in basedata[startdatastate]:
        if eachstate not in states:
            dropstates.append(eachstate)
    for eachstate in newdf[newdatastate]:
        if eachstate not in states:
            dropstates.append(eachstate)
    #Drop nondesired states
    basedata = basedata.loc[~basedata[startdatastate].isin(dropstates)]
    newdf = newdf.loc[~newdf[newdatastate].isin(dropstates)]
    #Merge datasets
    mergeddata=basedata.merge(newdf, left_on=startdatastate, right_on=newdatastate)
    #write out file
    result=mergeddata.to_csv(newfilename)
    #return final dataframe
    return result

