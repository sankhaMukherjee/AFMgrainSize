# ########################################################################
# This is version 3.0.
# In this version, the detection of the 'Scan size' has become a little 
#  more sophisticated. In the older program, it would look at the data
#  file for the following information:
#         1. The presence of the words Scan size
#         2. three elements after the second split with ':'
#     Hence, the following are proper parses of the previous data:
#         Scan size: 1 2 nm 
#         kdsjflsdf Scan size: 1 2 lkasdfjslf
#         "\Scan size: 1 2 lkasdfjslf"
#
# In the new version, we want to change the format so that the Scan size
#   parameter will now differ so that it will check for the following
#   criterion:
#     1. The line contains the words Scan size:
#     2. The portion of the line after Scan size can be split into either 2 or 3 words
#         2.1. The last word must contain nm or nm"
#         2.2. The remaining 1 or two words must comprise of numbers only
#   Hence, the following are allowed
#     Scan size: 12 34 nm"
#     aksddScan size: 12 nm
#
#   The following are not allowed:
#     Scan size 12 23 nm
#     Scan size: 12 34 ~m 
#     "\Scan size: 1 2 lkasdfjslf"
#     "\Scan size: 0 0 ~m"
#
#
# ########################################################################
import numpy as np

VERBOSE = True

def scanMatch(line):
    line = line.strip()
    if ('Scan size:' not in line) and ('Scan Size' not in line): return False
    if VERBOSE: print 'Line scan : [' + line + ']'
    if VERBOSE: print 'Pass 0'
    vals = line.split(': ')[1].split(' ')
    if (len(vals) < 2): return False
    if VERBOSE: print 'Pass 1'
    if (len(vals) > 3): return False
    if VERBOSE: print 'Pass 2'
    if vals[-1] not in ['nm', 'nm"']: return False
    if VERBOSE: print 'Pass 3'
    if not vals[0].isdigit(): return False
    if VERBOSE: print 'Pass 4'
    if len(vals) == 3 and not vals[1].isdigit(): return False
    if VERBOSE: print 'All pass'

    return True

def parseScan(l):
    vals = l.split(': ')[1].split(' ')
    if len(vals) == 2:
        return float(vals[0]), float(vals[0]), 'nm'
    else:
        return float(vals[0]), float(vals[1]), 'nm'

def readAFMfile( fileName ):
    """
        This function takes the name of a file created using the
        AFM software and then returns a numpy array. It does not
        do any check to see of the file has a problem or not. 
        Figuring that out is your problem. 
    """
    data       = []
    xLim, yLim = -1, -1
    unit       = 'a.u.'
    scanLine   = 'Match for scan line : Not found'
    
    with open(fileName, 'r') as f:
        
        # Skip the header
        while True:
            l = f.readline()
            
            # Parse the Scan size: line
            if scanMatch(l): 
                xLim, yLim, unit = parseScan(l)
                scanLine         = '# ----> Match for scan line: [' + l + ']'
                
            if l.find('File list end') > -1: break
        
        # This is the one line that is blank ...
        f.readline() 
        
        # get the data ...
        for l in f.readlines():
            if len(l.split()) <10: break
            #print 'Data Line: ', l
            data.append( np.array(map(float, (l.split())) ))
            
    data = np.array(data);
    
    if xLim == -1:
        print '+------------------------------------------------------+' 
        print '|  Error: Unable to find the Scan size ...             |'
        print '|         Changing the scale to the shape of the data  |'
        print '|         The results will have arbitrary units ...    |'
        print '+------------------------------------------------------+' 
        yLim, xLim = np.shape(data)
    else:
        print scanLine
            
    return xLim, yLim, data, unit
    

    
