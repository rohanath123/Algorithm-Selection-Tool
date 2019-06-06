import pandas as pd
import numpy as np

class EasyData:
    def __init__(self,path):
        '''
        Simple Path initalisation and creating the main
        data frame.
        '''
        self.mainFrame = pd.read_csv(path)
        self.makeEasyData()

    def makeEasyData(self):
        '''
        Gets the columns
        Seprates out the Target Column(As of now assumed as the first column)
        Gets the Columns with NaN error.

        **Instead want to do this: Study each column. Perform optimisation operation
          on it such as Normalisation, Cleaning(If Nans), Seprating the columns **
        '''
        columns = list(self.mainFrame.columns)
        self.y_labels = np.array(self.mainFrame[columns[0]].tolist())
        nanList = self.getNanList(columns[1:])

    def getNanList(self,columns):
        '''
        Takes the columns and returns a list of column names which have a
        NaN values in them.
        '''
        nanList = []
        for col in columns:
            naCount = sum(pd.isna(self.mainFrame[col]))
            if(naCount > 0):
                nanList.append(col)