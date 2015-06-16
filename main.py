'''
Created on Jun 8, 2015

@author: jyhu
'''


import os


from TouchzoneExtract import *
from FeatureStatistic import *
from CurveSimulator import *

  
if __name__ == '__main__':
    touchzone = TouchzoneExtract(r"C:\Users\jyhu\Downloads\subject\SD\src\log\accuracy\24mm\nsd.csv", 13, 23, 0.3)
    statistic = FeatireStatistic(touchzone)
       
#     touchzone1 = TouchzoneExtract(r"C:\Users\jyhu\Downloads\subject\SD\src\log\accuracy\24mm\27pf.csv", 13, 23, 0.3)
#     statistic1 = FeatireStatistic(touchzone1)
    
#     touchzone2 = TouchzoneExtract(r"C:\Users\jyhu\Downloads\subject\SD\src\log\accuracy\24mm\62pf.csv", 13, 23, 0.3)
#     statistic2 = FeatireStatistic(touchzone2)
     
    touchzone3 = TouchzoneExtract(r"C:\Users\jyhu\Downloads\subject\SD\src\log\accuracy\24mm\100pf.csv", 13, 23, 0.3)
    statistic3 = FeatireStatistic(touchzone3)
    
    curve1 = CurveSimulator(statistic, statistic3)
    curve1.simulate_matrix_diff_rx()
    