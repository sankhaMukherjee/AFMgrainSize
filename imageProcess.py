# ########################################################################
# This is version 3.0.
# We see if we can improve the performance of the delete points
# so that we can get some improvement in measurement time ...
# ########################################################################

from scipy.ndimage.filters import median_filter, convolve
from scipy.spatial         import Voronoi, voronoi_plot_2d
import numpy               as     np
import pylab               as     pl
import subprocess          as     subP


def peakFind(d, threshold=-1, filt=np.ones((5,5)), edge=1):
    """
        This function takes an array and finds all the local minima
        in the matrix. Input requirements:
        
        d         = 2D NumPy array that you want to find peaks in
        threshold = the minimum value below which everything is going
                    to be made equal to 0
        filt      = This is the filter that will be used for the
                    convolution. 
        edge      = number of pixels that wou want to neglect from the 
                    edge of the figure. The edge has to be greater than
                    0. A 0 for edge will throw an error. 
        
        Return values:
        
        (r,c) = values of the row/column numbers that contain the 
                max positions
    """
    d = d - d.min()
    
    R, C = np.shape(d)
    
    ptsR, ptsC = [], []
    
    # First, do a median filtering
    d = median_filter(d, size=3)
    
    # Now do some thresholding if necessary
    if threshold > -1: d[ d <= threshold ] = 0
    
    # Smoothing filter
    d = convolve(d, filt)
    
    # Find the peak using the local Maxima approach. 
    # For each position scanned, it will check to see 
    # if it is the largest value among its nearest neighbors
    for i in range(edge, R-edge+1):
        for j in range(edge, C-edge+1):
            if d[i,j] > d[i-1, j-1] and \
               d[i,j] > d[i-0, j-1] and \
               d[i,j] > d[i+1, j-1] and \
               d[i,j] > d[i-1, j-0] and \
               d[i,j] > d[i+1, j-0] and \
               d[i,j] > d[i-1, j+1] and \
               d[i,j] > d[i-0, j+1] and \
               d[i,j] > d[i+1, j+1] :
               
               ptsR.append(i)
               ptsC.append(j)
                
                
    return np.array(ptsR), np.array(ptsC)
    
def deleteClosePoints(x, y, fact = 0.25):
    """
        This function is going to take values of x and y and 
        then group values which are too close to one another
        as one point. This helps us make sure that the point
        we select are in fact separate grains, and not part
        of the same grain. 
        
        Quantitative descripton:
        Let p = the maximum value of the distance between two
        nearest neighbor points. Then, any nearest-neighbor
        point that is less than p/4 is considered to be part 
        of the same grain. 
        
        Input: 
        x,y = list of points that are supposed to be the center 
              of a grain.
        fact = the factor (default 0.25) that will determine how 
               far a grain has to be to be considered a separate 
               grain
        
        Return:
        x,y = list of points from which points which are too close
              have been removed...
    """


    X, Y = np.meshgrid(x, y)
    delX, delY = X - X.T, Y - Y.T
    dist = np.sqrt( delX*delX + delY*delY  )
    dist = dist + np.eye(len(x)) * dist.max()
    
    nnDist = np.array([ d.min() for d in dist ])
    nnDM   = nnDist.max()
    nnMin  = nnDM*fact # the minimum allowed distance

    
    # ---------------------------------------------------
    # We are grouping points here. Later we will need
    # to rearrange points so that it is a list of 
    # points and not a list of Lists
    # ---------------------------------------------------
    ptsLL = [] #  -> [ [(x11, y11), (x12, y12), ..], 
               #       [(x11, y11), (x12, y12), ..],
               #     ...]
    
    if dist.min() > nnMin: return (x, y), nnDist
    else:
        # We actually need to calculate stuff ....
        for xi, yi in zip( x, y ):
            if ptsLL == []: ptsLL = [[(xi, yi)]]
            else: 
                pos = -1
                for i, pl in enumerate(ptsLL):
                    # pl is a list of (x,y)
                    # check to see if (xi, yi) fits in this list.
                    # if it does, then note the position to insert
                    # this point in, and rbeak out of here
                    xL, yL = zip(*pl);
                    xL = np.array(xL); yL = np.array(yL); 
                    mDist = (np.sqrt( (xL-xi)**2 + (yL - yi)**2 )).min()
                    if mDist < nnMin: 
                        pos = i
                        break
                        
                if pos > -1: ptsLL[pos].append( (xi, yi) )
                else:        ptsLL.append([(xi, yi)])
                
        # Here, we need to convert the List of Lists to a single List
        ptsL = []
        for pl in ptsLL:
            if len(pl) == 1: 
                ptsL.append( pl[0] )
            else:
                xL, yL = zip(*pl)
                xL, yL = np.array(xL), np.array(yL)
                ptsL.append( (xL.mean(), yL.mean()) )
            
                    
    x, y = map(np.array, zip(*ptsL))

    X, Y = np.meshgrid(x, y)
    delX, delY = X - X.T, Y - Y.T
    dist = np.sqrt( delX*delX + delY*delY  )
    dist = dist + np.eye(len(x)) * dist.max()
    
    nnDist = np.array([ d.min() for d in dist ])
    
    return map(np.array, zip(*ptsL)), nnDist
    
def findVoronoi(x,y):
    '''
        This function is used for finding the points which
        form voronoi patches. The input are a number of x,y
        coordinates, while the output is the vertices and a
        list of list containing how the vertices are connected.
        
        This function will return all patches. Even those which
        are outside the image which is originally supplied. It
        is up to the user to make sure that such values are 
        eliminated during the clauclations ...
        
    '''
    points = np.array( map(list, zip(x,y)) )
    vor   = Voronoi(points)
    vData = vor.vertices
    pData = vor.regions
    
    return vData, pData, vor.point_region
    
def pointInPatch(x,y,poly):
    '''
        This function takes a point x,y and determines if it 
        lies inside the polygons determined by the vertices of
        the patch. We do 2 levels of checks. In the first level
        we see if a point is outside the min/max values of the 
        patch. Then and only then do we proceed for the next test.
        
        The patch is a list that looks like so: [(float, float)]
    '''

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def whichPoint(points, poly):
    '''
        Given a set of points, this will determine which one
        is inside the poly
    '''
    for p in points:
        if pointInPatch(p[0], p[1], poly): return p
        
    # We come here if nothing is returned
    return (-1, -1)