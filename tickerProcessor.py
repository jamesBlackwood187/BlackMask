from pandas.io.data import DataReader
import os
import pandas as pd
import numpy as np
from datetime import datetime


def GetOpenPrices(ticker,startDate, endDate):
   fullHistory =  DataReader(ticker,  'yahoo', startDate, endDate)
   priceHistory = pd.DataFrame()
   priceHistory['Open'] = fullHistory['Open']
   return priceHistory
   
def DifferenceSeries(tickDF):
    tickDF['dOpen'] = tickDF - tickDF.shift(1)
    tickDF = tickDF.dropna()
    return tickDF

def logTransform(tickDF):
    tickDF['logTransform'] = np.sign(tickDF['dOpen']) * (np.log(np.absolute(tickDF['dOpen'])) + 1)
    tickDF = tickDF.dropna()
    return tickDF

def delayEmbed(tickDF, dimension):
    for ind in range(len(tickDF)):
        if ind < dimension:
            continue
        else:
            delayVec = np.zeros(dimension)
            for i in range(dimension):
                delayVec[i] = tickDF.iloc[ind - dimension + i]['logTransform']
            print(delayVec)
            tickDF.iloc[ind]['Sig'] = delayVec
    return tickDF
            
        
    


nug = GetOpenPrices('NUGT',datetime(2012,1,1), datetime(2020,8,19))
nug = DifferenceSeries(nug)
nug = logTransform(nug)
nug = delayEmbed(nug,2)
print(nug)