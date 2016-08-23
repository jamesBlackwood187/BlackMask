from pandas.io.data import DataReader
from skrvm import RVR
from modwt import modwt, modwtmra
import os
from datetime import datetime
import numpy as np
import pywt




def GetPrices(ticker,startDate, endDate):
   priceHistory =  DataReader(ticker,  'yahoo', startDate, endDate)
   return priceHistory
   
def GenerateReturns(priceHistoryDF):
    priceHistoryDF['Returns'] = (priceHistoryDF['Close'] / priceHistoryDF['Open']) - 1
    return priceHistoryDF
    
def GenerateLaggedReturns(tickerDF):
    tickerDF['lagReturns'] = tickerDF.Returns.shift(1)
    return tickerDF

def GenerateFullTickerDF(ticker):
    pricePull = GetPrices(ticker,datetime(2012,1,1), datetime(2020,8,19))
    tickerDF = GenerateReturns(pricePull)
    tickerDF = GenerateLaggedReturns(tickerDF)
    if (len(tickerDF) % 2 == 0):
        tickerDF = tickerDF.fillna(0)
    else:
        tickerDF = tickerDF.dropna()
    return tickerDF

def swtLagReturns(tickDF):
    dataSet = tickDF['lagReturns']
    swt = pywt.swt(dataSet, wavelet = 'db8', level = 1)
    swt1 = swt[0][0]
    swt2 = swt[0][1]
    tickDF['swt1'] = swt1
    tickDF['swt2'] = swt2
    return tickDF

def mraLagReturns(tickerDF, mraLevel):
    wt = modwt(tickerDF['lagReturns'],'db8', mraLevel)
    wtmra = modwtmra(wt, 'db8')
    for i in range(mraLevel + 1):
        name1 = 'v'+ str(i)
        tickerDF[name1] = wtmra[i]
    return tickerDF

def VirginTrainAndPredict(tickerDF):
    tickerDF = mraLagReturns(tickerDF,1)
    predPoint = tickerDF.tail(1)
    predPointInputs = tickerDF.tail(1)[['v0','v1']]
    trainDF = tickerDF.ix[:-1]
    print(tickerDF)
    print(trainDF)
    trainTargets = trainDF['Returns']
    trainInputs = trainDF[['v0','v1']]
    clf = RVR(kernel = 'rbf')
    clf.fit(trainInputs, trainTargets)
    currPred = clf.predict(predPointInputs)
    return currPred
    
def T1robustTrainAndPredict(tickerDF):
   returnSpace = np.linspace(-0.5,0.5,25)
   for simRet in returnSpace:
       lagReturnSet = tickerDF['lagReturns'].values
       lagReturnSet = np.append(lagReturnSet, np.array(simRet))
       print(lagReturnSet)
   return     

ticker = 'NUGT'
nug = GenerateFullTickerDF(ticker)
#nug = VirginTrainAndPredict(nug)
T1robustTrainAndPredict(nug)