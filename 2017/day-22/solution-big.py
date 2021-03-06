import numpy as np
from aocd import get_data

raw = get_data(day=22,year=2017)
data = np.array([ [ c == '#' for c in line.strip()] for line in raw.splitlines() ], dtype=int)
center = [len(data)//2,len(data)//2]
def extend(data, loc):
    if(loc == 'top'):
        center[0] += 2
        return np.vstack((np.zeros_like(data[:2,:]), data))
    if(loc == 'bot'):
        return np.vstack((data, np.zeros_like(data[:2,:])))
    if(loc == 'left'):
        center[1] += 2
        return np.hstack((np.zeros_like(data[:,:2]), data))
    if(loc == 'right'):
        return np.hstack((data, np.zeros_like(data[:,:2])))
pos = len(data)//2+len(data)//2 *1j
vel =0-1j
def burst(data, pos,vel):
    x,y = int(pos.real),int(pos.imag)
    if(data[y,x] == 1): #infected
        vel *= 1j
        data[y,x] = 2 #F
        rval = 0
    elif(data[y,x] == 0): #clean
        vel *= -1j
        data[y,x] = 3 #W
        rval = 0
    elif( data[y,x] == 2): #flagged
        vel *= -1
        data[y,x] = 0 # C
        rval = 0
    elif( data[y,x] == 3): #weakened
        data[y,x] = 1 #I
        rval = 1
    pos += vel
    x,y = int(pos.real),int(pos.imag)
    if( x < 0 ):
        pos += 2
        data = extend(data, 'left')
    if( x >= data.shape[1] ):
        data = extend(data, 'right')
    if( y < 0 ):
        pos += 2j
        data = extend(data, 'top')
    if( y >= data.shape[0] ):
        data = extend(data, 'bot')
    return data, pos, vel, rval
infections = 0
for i in range(10000000):
    data, pos, vel, rval = burst(data, pos, vel)
    infections += rval
print('Part B: ', infections)
