import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def binning(data,sec=5,binning=5):
    '''
    Creates a binned light curves
    '''
    # Creates binning time in intervals of 5 seconds
    bins = sec/binning

    # creates a "seconds" column
    data['secs'] = data['dtmin']*60
    
    # Bins the original data table and creates a mean
    binned = data.groupby(np.arange(len(data))//bins).mean() 
    
    # Calculating error
    error = data['ure']**2
    binned['ure'] = np.sqrt(error.groupby(np.arange(len(error))//bins).sum())/bins

    return binned


def meanData(data):
    '''
    Calculates the mean mjd, flux density, and error of input data table
    '''
    mean_mjd = np.mean(data['mjd'])
    mean_flux = np.mean(data['re'])
    mean_err = np.sqrt(np.sum(data['ure']**2)/len(data))
    
    return mean_mjd,mean_flux,mean_err