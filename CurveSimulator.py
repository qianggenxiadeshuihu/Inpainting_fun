'''
Created on Jun 12, 2015

This class works as service routine after FeatureStatistic
@author: jyhu
'''
from ShowMatrix import *
from FeatureStatistic import *
import numpy
import matplotlib.pyplot as plot
from scipy.optimize import leastsq

class CurveSimulator(object):
    '''
    classdocs
    '''
    
    #indicate ax^2+bx+c
    DEGREE_OF_POLY = 3
    PLOT_PATTERN = {0:'yp', 1:'g-'}
    INIT_VALUE = 0

    def __init__(self, statistic_1, statistic_2):
        '''
        Constructor
        input parameters are matrix interpreted by dictionary
        '''
        if statistic_1.rx_number != statistic_2.rx_number or statistic_1.tx_number != statistic_2.tx_number :
            raise ErrorReport("compared touch zone should have same attributes")
       
        self.rx_number = statistic_1.rx_number
        self.tx_number = statistic_1.tx_number
        
        self.line_pattern = self.INIT_VALUE
        self.first_plot = self.INIT_VALUE
       
        #always use tz1 to stand for the non-SD (large signal) situation
        if statistic_1.get_sum() >= statistic_2.get_sum():
            self.tz1_rx = statistic_1.matrix_rx
            self.tz2_rx = statistic_2.matrix_rx
            
            self.tz1_tx = statistic_1.matrix_tx      
            self.tz2_tx = statistic_2.matrix_tx
        else:
            self.tz2_rx = statistic_1.matrix_rx
            self.tz1_rx = statistic_2.matrix_rx
            
            self.tz2_tx = statistic_1.matrix_tx      
            self.tz1_tx = statistic_2.matrix_tx
        
        self.init_matrix()
        
        self.get_matrix_diff_rx()
        
    def init_matrix(self):
        #init 
        self.tz_diff_rx = {}
        for i in xrange(self.rx_number):
            self.tz_diff_rx[i] = {}
            
        self.tz_diff_tx = {}
        for i in xrange(self.tx_number):
            self.tz_diff_tx[i] = {}
            
    def get_matrix_diff_rx(self):
#         for i in xrange(self.rx_number):
#             for j in xrange(self.tx_number):
#                 if self.tz1_rx.has_key(i) and self.tz2_rx.has_key(i):
#                     if self.tz1_rx[i].has_key(j) and self.tz2_rx[i].has_key(j):
#                         self.tz_diff_rx[i][j] = self.tz1_rx[i][j] - self.tz2_rx[i][j]
#                     elif not self.tz1_rx[i].has_key(j) and not self.tz2_rx[i].has_key(j):
#                         pass
#                     else:                        
#                         raise ErrorReport("sizes of matrixs are different : tx diff ")
#                 else:
#                     raise ErrorReport("sizes of matrixs are different2 : rx diff")
        self.tz_diff_rx = self.tz1_rx
    
    def get_matrix_diff_tx(self):
        for i in xrange(self.tx_number):
            for j in xrange(self.rx_number):
                if self.tz1_tx.has_key(i) and self.tz2_tx.has_key(i):
                    if self.tz1_tx[i].has_key(j) and self.tz2_tx[i].has_key(j):
                        self.tz_diff_tx[i][j] = self.tz1_tx[i][j] - self.tz2_tx[i][j]
                    elif not self.tz1_tx[i].has_key(j) and not self.tz2_tx[i].has_key(j):
                        pass
                    else:                        
                        raise ErrorReport("sizes of matrixs are different : tx diff ")
                else:
                    raise ErrorReport("sizes of matrixs are different2 : rx diff")
                
    def show_matrix_diff_rx(self):
        ShowMatrix(self.tz_diff_rx, ShowMatrix.RX_DOMAIN, self.rx_number, self.tx_number).show_matrix()
    
    def show_matrix_diff_tx(self):
        ShowMatrix(self.tz_diff_tx, ShowMatrix.TX_DOMAIN, self.rx_number, self.tx_number).show_matrix()
        
    def simulate_matrix_diff_rx(self):
        self.get_matrix_diff_rx()
        for i in xrange(self.rx_number):
            if self.tz_diff_rx.has_key(i) and self.tz_diff_rx[i] != {}:
                #here range is used instead of xrange
                x = range(len(self.tz_diff_rx[i]))
                #to have right sensor seris
                start_of_x = self.tz_diff_rx[i].keys()[0]
                x = [s+start_of_x for s in x]
                y = self.tz_diff_rx[i].values()
                para = self.leastsq_calculation(x, y)
                self.plot_simulate_result(x, y, para)
        plot.show()
    
    def simulate_matrix_diff_tx(self):
        self.get_matrix_diff_tx()
        for i in xrange(self.tx_number):
            if self.tz_diff_tx.has_key(i) and self.tz_diff_tx[i] != {}:
                #here range is used instead of xrange
                x = range(len(self.tz_diff_tx[i]))
                #to have right sensor seris
                start_of_x = self.tz_diff_tx[i].keys()[0]
                x = [s+start_of_x for s in x]
                y = self.tz_diff_tx[i].values()
                print y
                para = self.leastsq_calculation(x, y)
                print sum(self.residual(para[0], y, x))
                self.plot_simulate_result(x, y, para)
        plot.show()
                   
    def plot_simulate_result(self, real_x, real_y, para):
        
        simu_y = [self.fit_func(para[0], x) for x in real_x]

        if (self.first_plot == 0):
            plot.plot(real_x, simu_y, self.PLOT_PATTERN[1], label = "simulated data"
              , linewidth = 2)
            plot.plot(real_x, real_y, self.PLOT_PATTERN[0], label = "actual data"
              , linewidth = 2)
            self.first_plot += 1
        else:
            plot.plot(real_x, simu_y, self.PLOT_PATTERN[1]
              , linewidth = 2)
            plot.plot(real_x, real_y, self.PLOT_PATTERN[0]
              , linewidth = 2)

#         plot.title(": %f"%leastsq_result[0])
        plot.xlabel("sensor seris")
        plot.ylabel("rawcount")
        plot.legend()
#        plot.show()
                  
    def fit_func(self, p, x):
        f = numpy.poly1d(p)
        return f(x)
    
    def residual(self, p, y, x):
        return abs(y - self.fit_func(p, x))
    
    #real x and real y
    def leastsq_calculation(self, x, y):
        random_start = numpy.random.random(self.DEGREE_OF_POLY)
        coef = leastsq(self.residual, random_start, args=(y, x))
        return coef
        
        