'''
Created on Jun 17, 2015

@author: jyhu
'''
from DataLog import *

class Coord(object):
    def __init__(self, rx, tx):
        self.rx = rx
        self.tx = tx
        
        
class TouchzoneShape(object):
    '''
    classdocs
    '''
    
    #eight adjecent 
    EIGHT_ADJ = {
                0: Coord(-1, 0),
                1: Coord(-1, -1),
                2: Coord(0, -1),
                3: Coord(1, -1),
                4: Coord(1, 0),
                5: Coord(1, 1),
                6: Coord(0, 1),
                7: Coord(-1, 1)
                }
    
    FOUR_ADJ = {
                0: Coord(-1, 0),
                1: Coord(0, -1),
                2: Coord(1, 0),
                3: Coord(0, 1),
                }    
    
    INV = -65536
    SEED_NUM = 5

    def __init__(self, path, rx_number, tx_number):
        '''
        Constructor
        '''
        self.path = path
        self.rx_number = rx_number
        self.tx_number = tx_number
        
        #touchzone stored in [[]] for edge-peaks collection
        self.touchzone_frame = [[] for i in range(self.rx_number)]
        
        self.processed_frame = [[self.INV for j in range(self.tx_number)] for i in range(self.rx_number)]
        
        self.values = []
        
        self.seed = {}
        
        self.edge_peaks = []
    
    def print_frame(self, frame):
        for a_list in frame:
            for i in a_list:
                if i == self.INV:
                    print "%5d"%0,
                else:
                    print "%5d"%i,
            print ""
    
    def get_candidate_coord(self, cur, adj, adj_dict):
        ret_coord = Coord(-1, -1)
        ret_coord.rx = cur.rx + adj_dict[adj].rx
        ret_coord.tx = cur.tx + adj_dict[adj].tx
        return ret_coord
    
    def valid_edge_peak(self, temp_coord, cur):
        if self.touchzone_frame[temp_coord.rx][temp_coord.tx] >= self.touchzone_frame[cur.rx][cur.tx] / 2:
            for direction in range(len(self.FOUR_ADJ)):
                temp = self.get_candidate_coord(temp_coord, direction, self.FOUR_ADJ)
                if temp.rx in range(self.rx_number) and temp.tx in range(self.tx_number):
                    # for the sensors already identified as edge-peak, do not included in comparison
                    if self.processed_frame[temp.rx][temp.tx] != self.INV or \
                        self.touchzone_frame[temp_coord.rx][temp_coord.tx] >= self.touchzone_frame[temp.rx][temp.tx]:
                        continue
                    else:
                        return False
                else:#do not process for sensor out of panel
                    continue
            return True 
        else:
            return  False
    
    def generate_seed(self):
        self.seed_find_biggest()
        for s in range(self.SEED_NUM):
            self.edge_peaks.append(self.seed[s])
            self.processed_frame[self.seed[s].rx][self.seed[s].tx] = self.touchzone_frame[self.seed[s].rx][self.seed[s].tx]

             
    #This function finds all the edge-peaks in touch zone
    def extract_touchzone_by_region_growing(self):
        self.organize_touchzone()
        self.generate_seed()
        while self.edge_peaks != []:
            cur = self.edge_peaks.pop()
            for adj in range(len(self.EIGHT_ADJ)):
                temp_coord = self.get_candidate_coord(cur, adj, self.EIGHT_ADJ)
                if temp_coord.rx in range(self.rx_number) and temp_coord.tx in range(self.tx_number):
                    
                    if self.processed_frame[temp_coord.rx][temp_coord.tx] != self.INV:#do not do repeat and extra finding
                        continue
                    if self.valid_edge_peak(temp_coord, cur):
                        self.edge_peaks.append(temp_coord)
                        self.processed_frame[temp_coord.rx][temp_coord.tx]= self.touchzone_frame[temp_coord.rx][temp_coord.tx]
                    else:#not a local peak
                        continue            
                else:#do not process for sensor out of panel
                    pass
                
        self.print_frame(self.processed_frame)
        print self.judge_closed_touchzone()            

    def judge_closed_touchzone(self):
        start_point = self.seed[0]
        cur_point = Coord(start_point.rx, start_point.tx)
        prev_point = Coord(self.INV, self.INV)

        count = 0
        while True:
            max_diff_neigh = self.INV
            max_diff_neigh_dict = Coord(self.INV, self.INV)
            for direction in range(len(self.EIGHT_ADJ)):
                temp_rx = cur_point.rx + self.EIGHT_ADJ[direction].rx
                temp_tx = cur_point.tx + self.EIGHT_ADJ[direction].tx
                if temp_rx in range(self.rx_number) and temp_tx in range(self.tx_number) \
                        and (temp_rx != prev_point.rx or temp_tx != prev_point.tx):
                    
                    
                    if self.processed_frame[temp_rx][temp_tx] != self.INV:
                        if self.processed_frame[temp_rx][temp_tx] > max_diff_neigh:
                            max_diff_neigh_dict.rx = temp_rx
                            max_diff_neigh_dict.tx = temp_tx
                            max_diff_neigh = self.processed_frame[temp_rx][temp_tx]
            
            if max_diff_neigh != self.INV:
                prev_point.rx = cur_point.rx
                prev_point.tx = cur_point.tx
                cur_point.rx = max_diff_neigh_dict.rx
                cur_point.tx = max_diff_neigh_dict.tx
                print self.processed_frame[cur_point.rx][cur_point.tx]
            else:
                return False
            count += 1
            
            if count > 5 and (abs(cur_point.rx - start_point.rx) <= 1 and abs(cur_point.tx - start_point.tx) <= 1):
                return True
                

    def organize_touchzone(self):
        log = DataLog(self.path, self.rx_number, self.tx_number)
        self.values = log.load_log()
        #note: int32 should be carefully considered in porting to embedded system
        self.values = numpy.array(self.values, dtype=numpy.int32)     
        
        temp_line = []
        
        for i in xrange(self.rx_number):
            for j in xrange(self.tx_number):
                temp_line.append(self.values[i*self.tx_number + j])
            self.touchzone_frame[i] = temp_line
            temp_line = []
        
        
        self.print_frame(self.touchzone_frame)
        
    def seed_find_biggest(self):
        for i in xrange(self.rx_number):
            for j in xrange(self.tx_number):
                diffcount = self.touchzone_frame[i][j]
                
                #find ranking position    
                for s in range(self.SEED_NUM):
                    #find empty slot
                    if not self.seed.has_key(s) :
                        self.seed[s] = Coord(i, j)
                    elif self.touchzone_frame[i][j] > self.touchzone_frame[self.seed[s].rx][self.seed[s].tx]:
                        self.shift_seed_right(s)
                        self.seed[s].rx = i
                        self.seed[s].tx = j
                        break
                    else:
                        pass
        self.print_seed()
        
    def shift_seed_right(self, s):
        k = self.SEED_NUM
        while k > s :
            if not self.seed.has_key(k):
                k -= 1
                continue
            else :
                self.seed[k].rx = self.seed[k-1].rx
                self.seed[k].tx = self.seed[k-1].tx
                k -= 1
        
    def print_seed(self):
        print "seed:"
        for s in range(self.SEED_NUM):
            if self.seed.has_key(s) :
                print "<"+str(self.seed[s].rx)+", "+str(self.seed[s].tx)+", "+str(self.touchzone_frame[self.seed[s].rx][self.seed[s].tx])+">"