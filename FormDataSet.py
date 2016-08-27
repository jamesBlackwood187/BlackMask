import pandas as pd
import numpy as np
from datetime import datetime
import os

def getFiles(PATH):
	csvs = []
	for file in os.listdir(PATH):
		if file[-3:] == 'csv':
			csvs.append(file)
	return csvs
	


if __name__ == "__main__":
    csvList = getFiles(os.getcwd())
    print(csvList)
    for i in range(len(csvList)):
        currCSV = csvList[i]
        if i == 0:
            colName1 = "logReturn" + str(currCSV[:-4])
            masterDF = pd.read_csv(currCSV, header = 0, usecols=[0,3], names = ['Date', colName1])
        else:
            colName1 = "logReturn" + str(currCSV[:-4])
            thisDF = pd.read_csv(currCSV, header = 0, usecols=[0,3], names = ['Date', colName1])
            masterDF = pd.merge(thisDF, masterDF, on=['Date'])
    masterDF['Label'] = np.floor(300*masterDF['logReturnGLD'])
    
    targetSet = masterDF[ ['Date', 'Label'] ]
    gldReturn = masterDF[['Date', 'logReturnGLD']]
    masterDF = masterDF.drop('Label', 1)
    print(masterDF)
    
    
    lookBack = 50
    for i in range(lookBack + 1, len(masterDF)):
        os.chdir('/home/ubuntu/workspace/finance/BlackMask/DataSet')
        currDate = masterDF.iloc[i]['Date']
        pastDF = masterDF.iloc[i-lookBack:i]
        pastDF.to_csv(currDate+'.csv', index = False, sep = ',')
    targetSet.to_csv('targets.csv', index = False, sep = ',')
    gldReturn.to_csv('gldReturn.csv', index = False, sep = ',')
    os.chdir('/home/ubuntu/workspace/finance/BlackMask/')