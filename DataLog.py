'''
Created on Jun 17, 2015

@author: jyhu
'''
import numpy
import os
import csv

class DataLog(object):
    '''
    classdocs
    '''
    #format of csv, no need to modify unless TTHE changes the format of log file
    #used as static member variables
    NO_USE_LINES_CSV = 3
    DATA_BEGIN_IN_ROW = 2

    def __init__(self, path, rx_number=13, tx_number=22):
        '''
        Constructor
        '''
        self.path = path       
        self.rx_number = rx_number
        self.tx_number = tx_number
        
        self.values = []
        
    def load_log(self):
        try:            
            data_path = os.path.normpath(os.path.realpath(self.path))
            data = open(data_path,'r')
            line_index = 0
            for line in data:      
                line = line.replace('\n','')
                line = line.replace('\t','')
                cols = line.split(',')          
                if line_index == DataLog.NO_USE_LINES_CSV:    
                    #only capture the first line
                    self.values = (cols[DataLog.DATA_BEGIN_IN_ROW : 
                                   DataLog.DATA_BEGIN_IN_ROW + self.tx_number*self.rx_number])
                    break
                line_index += 1
            data.close()
            if self.values != []:
                return self.values
            else:
                print "nothing in the log file"
        except:
            print "pls double-check the path for log file"
    
    def print_log(self):
        print self.values