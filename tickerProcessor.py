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
    tickDF['dOpen'] = tickDF / tickDF.shift(1)
    tickDF = tickDF.dropna()
    return tickDF

def logTransform(tickDF):
    tickDF['logTransform'] = np.log(tickDF['dOpen'])
    tickDF = tickDF.dropna()
    return tickDF
    
def processTicker(tick):
    df = GetOpenPrices(tick, datetime(2012,1,1), datetime(2020,1,1))
    df = DifferenceSeries(df)
    df = logTransform(df)
    return df


if __name__ == "__main__":
    tickerList = ['SPY', 'EWJ', 'VXX', 'FXI', 'JPY=X', 'EUR=X', 'SHV', 'OIL', 'GLD']
    for ticker in tickerList:
        tickDF = processTicker(ticker)
        tickDF.to_csv(ticker+'.csv', sep = ',')
