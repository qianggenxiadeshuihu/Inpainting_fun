'''
Created on Jun 8, 2015

@author: jyhu
'''

from DataLog import *



class ElementTouchzone():
    
    def __init__(self):
        self.element_rx = 0
        self.element_tx = 0
        self.element_magnitude = 0
    
    def show(self):
        print "<" + str(self.element_rx) + ", " + str(self.element_tx) + ", " + str(self.element_magnitude) + ">"



class TouchzoneExtract(object):

    
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
        log = DataLog(self.path, self.rx_number, self.tx_number)
        self.values = log.load_log()
        print self.values
        self.extract_touchzone_by_multiplier()
        
    #load log from log.csv by TTHE        
    
    def print_touchzone(self):
        for i in self.touchzone_ori:
            i.show()

 
    #sd_multiplier is used to define touch zone. The value indicates bit number for right shift           
    def extract_touchzone_by_multiplier(self):
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
    
    
