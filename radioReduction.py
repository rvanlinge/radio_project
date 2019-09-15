import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import glob 

def binning(data,sec=5,binning=5):
    '''
    Creates a binned light curves
    '''
    # Filters out the bad data points
    data = data[data['nsamp']>np.mean(data['nsamp'])-(0.5*(np.mean(data['nsamp'])))]
    
    # Tells how many rows to bin in intervals of binning seconds
    bins = sec/binning
    
    # How many times can the data table be divided by binning time
    split = len(data)/bins   
    
    # Creates binned times
    data['secs'] = data['dtmin']*60
    
    avgSecs = []
    secs = data['secs']
    secsSplit = np.array_split(secs,split)
    
    for i in range(len(secsSplit)):
        avgSecs.append(np.mean(secsSplit[i]))
    
    
    # Calculating average MJD
    avgMjd = []
    
    mjd = data['mjd']
    mjdSplit = np.array_split(mjd,split)
    
    for i in range(len(mjdSplit)):
        avgMjd.append(np.mean(mjdSplit[i]))
    
    
    # Bins Flux
    avgFlux = [] # holds averaged flux values
    flux = data['re']
    fluxSplit = np.array_split(flux,split)
    
    for i in range(len(fluxSplit)):
        avgFlux.append(np.mean(fluxSplit[i]))
    
    # Bins uncert
    avgErr = []
    err = data['ure']
    errSplit = np.array_split(err,split)
    
    for i in range(len(errSplit)):
        x = errSplit[i]
        avgErr.append(1/np.sqrt(np.sum(1/x**2)))
    
    
    # Creating binned data frame
    binned = pd.DataFrame(data={'mjd':avgMjd,'dtmin':(np.array(avgSecs)/60),'secs':avgSecs,'re':avgFlux,'ure':avgErr})
    return binned

def meanData(data):

    data = data[data['nsamp']>np.mean(data['nsamp'])-(0.5*(np.mean(data['nsamp'])))]
    
    # Getting MJD value
    mean_mjd = np.mean(data['mjd'])
    
    # Calculating the average flu
    mean_flux = np.mean(data['re'])
    
    # calculating the average err
    mean_err = 1/np.sqrt(np.sum(1/data['ure']**2))
    
    return mean_mjd,mean_flux,mean_err

def scatterPlotting(x,y,uncert=0,Type=0):
    '''
    Type:
    0 = scatter
    1 = plot
    '''
    
    if Type == 0:
        if uncert == 0:
            plt.figure(figsize=(10,8))
            plt.scatter(x,y,color='k')
        if uncert != 0:
            plt.figure(figsize=(10,8))
            plt.errorbar(x,y,yerr=uncert,fmt='o',linestyle='None',color='k')
            
    return none
                
                
                
def lightCurve(path):
    '''
    Takes in a list of data tables and creates an average light curve
    '''
    
    # Holds the values
    re = []
    ure = []
    mjd = []
    
    
    # gathers all the data tables
    
    dt = glob.glob(path)
    
    for i in dt:
        x = pd.read_table(i)
        m,r,e = meanData(x)
        mjd.append(m)
        re.append(r)
        ure.append(e)
        
    new_dt = pd.DataFrame(data={'mjd':mjd,'re':re,'ure':ure})
    new_dt = new_dt.sort_values('mjd')
    new_dt = new_dt.reset_index(drop=True)
    
    return new_dt
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                