'''
Created on Jun 8, 2015

@author: jyhu
'''

import numpy
import os
import csv



class ElementTouchzone():
    
    def __init__(self):
        self.element_rx = 0
        self.element_tx = 0
        self.element_magnitude = 0
    
    def show(self):
        print "<" + str(self.element_rx) + ", " + str(self.element_tx) + ", " + str(self.element_magnitude) + ">"



class TouchzoneExtract(object):
    #format of csv, no need to modify unless TTHE changes the format of log file
    #used as static member variables
    NO_USE_LINES_CSV = 3
    DATA_BEGIN_IN_ROW = 2
    
    def __init__(self, path, rx_number=13, tx_number=22, sd_multiplier=1):
        #rx domain
        self.rx_number = rx_number
        self.tx_number = tx_number
        self.path = path
        #define touchzone
        self.sd_multiplier = sd_multiplier    
        
        #touchzone stored in list of tuple <txPos, rxPos, magnitude>
        #used as member variables
        self.touchzone_ori = []
        
        #values stores for original data from log.csv
        self.values = []             
    
        self.process()
    
    def process(self):
        self.load_log()
        self.extract_touchzone()
        
    #load log from log.csv by TTHE        
    def load_log(self):
        try:            
            data_path = os.path.normpath(os.path.realpath(self.path))
            data = open(data_path,'r')
            line_index = 0
            for line in data:      
                line = line.replace('\n','')
                line = line.replace('\t','')
                cols = line.split(',')          
                if line_index == TouchzoneExtract.NO_USE_LINES_CSV:    
                    #only capture the first line
                    self.values = (cols[TouchzoneExtract.DATA_BEGIN_IN_ROW : 
                                   TouchzoneExtract.DATA_BEGIN_IN_ROW + self.tx_number*self.rx_number])
                    break
                line_index += 1
            data.close()
        except:
            print "pls double-check the path for log file"
    
    def print_log(self):
        print self.values
    
    def print_touchzone(self):
        for i in self.touchzone_ori:
            i.show()
   
    #sd_multiplier is used to define touch zone. The value indicates bit number for right shift           
    def extract_touchzone(self):
        #note: int32 should be carefully considered in porting to embedded system
        self.values = numpy.array(self.values, dtype=numpy.int32)
        max_val = max(self.values)        
        
        for i in xrange(len(self.values)):
            if self.values[i] >= (max_val * self.sd_multiplier):
                element_touchzone = ElementTouchzone()
                element_touchzone.element_rx = i/self.tx_number
                element_touchzone.element_tx = i - element_touchzone.element_rx * self.tx_number
                element_touchzone.element_magnitude = self.values[i]
                self.touchzone_ori.append(element_touchzone)
                
    
