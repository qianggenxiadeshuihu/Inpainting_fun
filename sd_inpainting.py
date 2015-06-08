'''
Created on Jun 8, 2015

@author: jyhu
'''

import numpy
import matplotlib.pyplot as plot
from scipy.optimize import leastsq
import pylab
import os
import csv
from __builtin__ import max
from numpy import dtype


class FeatureDetect(object):
    a=1
    
class ElementTouchzone():
    element_rx = 0
    element_tx = 0
    element_magnitude = 0
    
    def show(self):
        print "<" + str(self.element_rx) + ", " + str(self.element_tx) + ", " + str(self.element_magnitude) + ">"
     
class TouchzoneExtract(object):
    #format of csv, no need to modify unless TTHE changes the format of log file
    #used as static member variables
    NO_USE_LINES_CSV = 3
    DATA_BEGIN_IN_ROW = 2
    
    #rx domain
    rx_number=13
    tx_number=22
    
    #touchzone stored in list of tuple <txPos, rxPos, magnitude>
    #used as member variables
    touchzone_ori = []
    
    #values stores for original data from log.csv
    values = []  
    
    #load log from log.csv by TTHE        
    def load_log(self, path, rx_number=13, tx_number=22):

        if self.rx_number != rx_number:
            self.rx_number = rx_number
        if self.tx_number != tx_number:
            self.tx_number = tx_number
        
        data_path = os.path.normpath(os.path.realpath(path))
        data = open(data_path,'r')
        line_index = 0
        for line in data:      
            line = line.replace('\n','')
            line = line.replace('\t','')
            cols = line.split(',')          
            if line_index == TouchzoneExtract.NO_USE_LINES_CSV:    
                #only capture the first line
                self.values = (cols[TouchzoneExtract.DATA_BEGIN_IN_ROW : 
                               TouchzoneExtract.DATA_BEGIN_IN_ROW + tx_number*rx_number])
                break
            line_index += 1
        data.close()
    
    
    def print_log(self):
        print self.values
    
    def print_touchzone(self):
        for i in self.touchzone_ori:
            i.show()

    
    #sd_multiplier is used to define touch zone. The value indicates bit number for right shift           
    def extract_touchzone(self, sd_multiplier=1):
        self.values = numpy.array(self.values, dtype=numpy.int16)
        max_val = max(self.values)
        for i in xrange(len(self.values)):
            if self.values[i] >= (max_val >> sd_multiplier):
                element_touchzone = ElementTouchzone()
                element_touchzone.element_rx = i/self.tx_number
                element_touchzone.element_tx = i - element_touchzone.element_rx * self.tx_number
                element_touchzone.element_magnitude = self.values[i]
                self.touchzone_ori.append(element_touchzone)
                    
    
if __name__ == '__main__':
    touchzone = TouchzoneExtract()
    touchzone.load_log("C:\Users\jyhu\Downloads\subject\SD\src\sd_inpainting\log\log.csv")
    
    touchzone.extract_touchzone() 
    touchzone.print_touchzone() 
