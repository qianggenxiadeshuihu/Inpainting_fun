'''
Created on Jun 12, 2015

@author: jyhu

This class helps to show matrix organized by dictionary
'''

class ShowMatrix(object):
    '''
    classdocs
    '''
    RX_DOMAIN = 0
    TX_DOMAIN = 1

    def __init__(self, matrix, domain, rx_number, tx_number):
        '''
        Constructor
        '''
        self.matrix = matrix
        if domain == self.RX_DOMAIN :
            self.rx_number = rx_number
            self.tx_number = tx_number
        elif domain == self.TX_DOMAIN :
            self.tx_number = rx_number
            self.rx_number = tx_number
        else:
            raise ErrorReport("Only RX domain and TX domain are supported")
        
    def show_matrix(self):
        for i in xrange(self.rx_number):
            for j in xrange(self.tx_number):
                if self.matrix.has_key(i):
                    if self.matrix[i].has_key(j):
                        print "%4d"%self.matrix[i][j],
                    else:
                        print "%4d"%0,
                else:
                    print "%4d"%0,
            print ""
        