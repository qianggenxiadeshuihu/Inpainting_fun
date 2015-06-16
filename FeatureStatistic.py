'''
Created on Jun 8, 2015

@author: jyhu
'''
from numpy import average
from ShowMatrix import *

class ErrorReport(RuntimeError):
    def __init__(self, err):
        print err

class FeatireStatistic(object):
    '''
    classdocs
    '''
    
    #this needs to be modified based the worse SD condition needing to be compensated
    NO_ENOUGH_TOUCHZONE_ALERT = 5
    
    
    def __init__(self, touchzone):
        '''
        Constructor
        '''
        self.touchzone = touchzone.touchzone_ori
        self.rx_number = touchzone.rx_number
        self.tx_number = touchzone.tx_number
        
        #use dict to store the zsum of col/row by same tx/rx
        self.sum_in_rx = {}
        self.sum_in_tx = {}
        
        #use double-layer list to store each rx/tx
        self.init_matrix()
        
        self.sum = 0
        
        #use this to jugde the size of touchzone 
        self.involved_tx_number = 0
        self.involved_rx_number = 0
        
        #use this to record the centre line (both rx/tx directions) to process
        self.mid_tx_pos = 0
        self.mid_rx_pos = 0
        
        self.process()
        
    def process(self):
        print "---------------------------------------------------------"
        self.get_zone_size() 
        self.show_zone_size() 
#         self.get_sum_in_rx()
#         self.show_sum_in_rx()
#         self.get_sum_in_tx()
#         self.show_sum_in_tx()
#         self.get_sum()
#         self.show_sum()
        self.get_average("ave of rx ", self.sum_in_rx)
        self.get_average("ave of tx ", self.sum_in_tx)
        self.get_matrix_rx()
        self.get_matrix_tx()
        print "peak"
        print self.get_peak(self.matrix_rx[self.mid_rx_pos])
        print self.get_peak(self.matrix_tx[self.mid_tx_pos])
        self.show_matrix_rx()
    
    #this function should be called after self.get_zone_size
    def get_sum(self):
        for element_touchzone in self.touchzone:
            self.sum += element_touchzone.element_magnitude
        return self.sum
    
    def show_sum(self):
        print "sum of touchzone is"
        print self.sum        
    
        
    #this function should be called after self.get_sum_in_tx
    #in dict like this: {<0, ...>, <1, ...>, ..., <n-2, ...>, <n-1, ...>}
    #calculate average of them except <0, ...> and <n-1, ...>   
    def get_average(self, des, value_dict):
        ave = 0
        a_list = value_dict.items()
        print a_list
        for i in xrange(len(a_list)):
            if i == 0 or i == len(a_list) - 1:
                pass
            else :
                ave += (a_list[i])[1]
        print des + str(ave / (len(a_list)-2))
        
    def show_average(self):
        pass
    
    def init_matrix(self):
        #init 
        self.matrix_rx = {}
        for i in xrange(self.rx_number):
            self.matrix_rx[i] = {}
            
        self.matrix_tx = {}
        for i in xrange(self.tx_number):
            self.matrix_tx[i] = {}
    
    #rx domain
    def get_matrix_rx(self):    
        for element_touchzone in self.touchzone:
            self.matrix_rx[element_touchzone.element_rx][element_touchzone.element_tx] = element_touchzone.element_magnitude
        print self.matrix_rx   
    
    #tx domain
    def get_matrix_tx(self):    
        for element_touchzone in self.touchzone:
            self.matrix_tx[element_touchzone.element_tx][element_touchzone.element_rx] = element_touchzone.element_magnitude
        print self.matrix_tx  
        
    #rx domain
    def show_matrix_rx(self):
        ShowMatrix(self.matrix_rx, ShowMatrix.RX_DOMAIN, self.rx_number, self.tx_number).show_matrix()
            
    #get peak of dict
    def get_peak(self, a_dict):
        return max(a_dict.values())
        
    #sum of items having same rx    
    def get_sum_in_rx(self):
        for element_touchzone in self.touchzone:
            if self.sum_in_rx.has_key(element_touchzone.element_rx):
                self.sum_in_rx[element_touchzone.element_rx] += element_touchzone.element_magnitude
            else:
                self.sum_in_rx[element_touchzone.element_rx] = element_touchzone.element_magnitude
    
    #sum of items having same tx
    def get_sum_in_tx(self):
        for element_touchzone in self.touchzone:
            if self.sum_in_tx.has_key(element_touchzone.element_tx):
                self.sum_in_tx[element_touchzone.element_tx] += element_touchzone.element_magnitude
            else:
                self.sum_in_tx[element_touchzone.element_tx] = element_touchzone.element_magnitude
    
    def show_sum_in_rx(self):
        print "zum in rx:"
        print self.sum_in_rx
    
    def show_sum_in_tx(self):
        print "zum in tx:"
        print self.sum_in_tx
    
    #number of rx and tx are calculated 
    #mid of rx and tx are stored too
    def get_zone_size(self):
        max_rx = -1
        max_tx = -1
        min_rx = 65535
        min_tx = 65535
        
        for element_touchzone in self.touchzone:
            max_rx = max(max_rx, element_touchzone.element_rx)
            max_tx = max(max_tx, element_touchzone.element_tx)
            min_rx = min(min_rx, element_touchzone.element_rx)
            min_tx = min(min_tx, element_touchzone.element_tx)
                
        self.involved_rx_number = max_rx - min_rx + 1
        self.involved_tx_number = max_tx - min_tx + 1        
        if self.involved_rx_number < FeatireStatistic.NO_ENOUGH_TOUCHZONE_ALERT \
            or self.involved_tx_number < FeatireStatistic.NO_ENOUGH_TOUCHZONE_ALERT :
            raise ErrorReport("touch zone needs not to be compensated")
        #not acurate enough, aslo doesn't matter for large touch zone 
        self.mid_rx_pos = min_rx + self.involved_rx_number/2 
        self.mid_tx_pos = min_tx + self.involved_tx_number/2 
    
    def show_zone_size(self):       
        print self.involved_rx_number 
        print self.involved_tx_number 