# ########################################################################
# This is version 3.0.
# Nothing has changed in thsi version
# ########################################################################
import numpy as np
import pylab as pl
from scipy   import optimize

def polyArea2D(poly):
    total = 0.0
    N = len(poly)
    for i in range(N):
        v1 = poly[i]
        v2 = poly[(i+1) % N]
        total += v1[0]*v2[1] - v1[1]*v2[0]
    return abs(total/2)

def fitData(x, y):
    fitFunc = lambda p, x: p[0] * ( np.exp( -(x - p[1])**2 / (2*p[2]**2) )  )
    errFunc = lambda p, x, y: fitFunc(p, x) - y
    
    p0 = [y.max(), x[ np.where(y == y.max())[0][0] ], 0.3*(x.max() - x.min())  ]
    p1, success = optimize.leastsq(errFunc, p0[:], args=(x, y)  )
    
    return p1

def plotAFM(data, xLim, yLim, unit):

    r, c = np.shape(data)
    
    pl.figure(figsize = (4, 4*r/c))
    pl.axes([0.2, 0.22, 0.77, 0.75])
    
    pl.imshow(data, aspect = 'auto', origin = 'lower', extent=(0, xLim, 0, yLim), cmap=pl.cm.jet)
    pl.xlabel('('+unit+')')
    pl.ylabel('('+unit+')')
    #pl.xticks([]); pl.yticks([])
    pl.show()

def plotVoronoi(vData, pData, xLim, yLim):

    '''
        This function assumes that there is already some figure
        which has been plotted.
        
    '''
    
    areaList = []
    ptsList  = []
    for j, pD in enumerate(pData):
        if -1 in pD: continue
        if pD ==[] : continue
        pD1 = pD + [pD[0]]
        x, y = np.array([vData[i] for i in pD1]).T
        if any (x>xLim) or any (x<0) or any (y>yLim) or any (y<0): continue
        pl.plot(x,y, color='black')
        
        areaList.append( polyArea2D( zip(x,y) ) ) 
        ptsList.append( j )
        
    return areaList, ptsList
        
def plotHist(val, unit, xlabelValue):
    
    fitFunc = lambda p, x: p[0] * ( np.exp( -(x - p[1])**2 / (2*p[2]**2) )  )
    
    pl.figure(figsize = (4,3))
    pl.axes([0.2, 0.22, 0.77, 0.75])
    n, ar1, tempPatch = pl.hist(val, 30, color=(1, 0.3, 0.2), ec=(0.5,0.5, 0.5))
    
    areas = 0.5*(ar1[1:] + ar1[:-1])
    
    p0 = [n.max(), areas[ np.where(n == n.max())[0][0] ], 0.3*(areas.max() - areas.min())  ]
    p1 = fitData(areas, n)
    
    xNew = np.linspace(areas.min(), areas.max(), 100)
    yNew = fitFunc(p1, xNew)
    
    pl.plot(xNew, yNew, color='black', lw=2)
    pl.xlabel(xlabelValue + '(' + unit +')')
    pl.show()
    return p1
