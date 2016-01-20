#####################################################
# Version 3.0
# This version additionally outputs a list of 
#  areas and nearest-neighbors
#####################################################

from   plotFigures  import *
from   fileIO       import *
from   imageProcess import *
import pylab        as     pl
import numpy        as     np
import os
import time

pl.ion()

startTime = time.clock()

__VERBOSE__ = True

dirToRead = r'data'

allFiles = [f for f in os.listdir(dirToRead) if '.txt' in f]
if __VERBOSE__ : print allFiles


f     = open('summary.csv','w')
fArea = open('summary - SqrtAreaList.csv', 'w')
fNN   = open('summary - nnList.csv', 'w')

header = """
        ,   ,  Area,     ,   ,Height,    ,  ,Kurtosis, ,   , polygon vertices, , , nn Distance, ,, sqrt  Area
Sample  ,  A,  mean,  std,  A,  mean,  std,  A,  mean,  std,  A,  mean,  std,  A,  mean,  std,  A,  mean,  std\n"""

f.write(header)

for fileName in allFiles:

    temp = time.clock()
    if __VERBOSE__ : print '[Reading File]',
    if __VERBOSE__ : print os.path.join(dirToRead, fileName),

    
    xLim, yLim, data, unit = readAFMfile( os.path.join(dirToRead, fileName) )
    data = data - data.min()
    maxY, maxX = np.shape(data)
    print 'Time to read the file: ', time.clock() - temp
    
    plotAFM(data, xLim, yLim, unit)
    
    temp = time.clock()
    if __VERBOSE__ : print ',[Finding peaks]',
    r1, c1 = peakFind(data, threshold=data.max()/5, filt=np.ones((3,3)), edge=3)
    r1, c1 = r1+1, c1+1
    print 'Time to find local Minima: ', time.clock() - temp

    if __VERBOSE__ : print 'Reducing multiple-peak points'
    temp = time.clock()
    pos, nnDist = deleteClosePoints(r1, c1, fact = 0.25)
    print 'Time to delete selected points: ', time.clock() - temp
    r1, c1 = pos; 
    nnDist = np.array( nnDist )*yLim/maxY
    r, c   = r1*yLim/maxY, c1*xLim/maxX 
    pl.plot(c, r, '+', mfc='None', mec='black')

    if __VERBOSE__ : print ',[Finding Voronoi patches]',
    temp = time.clock()
    vData, pData, pts = findVoronoi(c,r)
    print 'Time to calculate voronoi tessletation: ', time.clock() - temp
    
    temp = time.clock()
    areaList, ptsList = plotVoronoi(vData, pData, xLim, yLim)
    print 'Time to calculate get arealist, and ptsList: ', time.clock() - temp
    
    if __VERBOSE__ : print ',[Finding the heights]',
    heightInfo   = []
    polyVertInfo = []
    
    temp = time.clock()
    for pts in ptsList:
        patch    = vData[pData[pts]]
        xPt, yPt = whichPoint(zip(c,r), patch)
        xPt, yPt = int(xPt*maxX/xLim), int(yPt*maxY/yLim)
        heightInfo.append( data[yPt][xPt] )
        polyVertInfo.append( len( patch ) )
        
    heightInfo = np.array(heightInfo)
    polyVertInfo = np.array(polyVertInfo)
    print 'Time to do statistics: ', time.clock() - temp

    pl.savefig(fileName[:-4]+'_2Dmap.png', dpi=300)

    if __VERBOSE__ : print ',[Calculating area statistics]'
    p1 = plotHist(areaList, unit + '$^2$', 'Area')
    pl.savefig(fileName[:-4]+'_AreaHist.png', dpi=300)
    
    p2 = plotHist(heightInfo, 'nm', 'Height')
    pl.savefig(fileName[:-4]+'_HeightHist.png', dpi=300)
    
    p3 = plotHist(heightInfo/areaList, unit, '"Kurtosis"')
    pl.savefig(fileName[:-4]+'_KurtHist.png', dpi=300)
    
    p4 = plotHist(polyVertInfo, '#', '# vertices')
    pl.savefig(fileName[:-4]+'_PatchHist.png', dpi=300)
    
    p5 = plotHist(nnDist, 'nm', 'nn distance')
    pl.savefig(fileName[:-4]+'_nnHist.png', dpi=300)
    
    p6 = plotHist(np.sqrt(areaList), unit , 'sqrt(Area)')
    pl.savefig(fileName[:-4]+'_SqrtAreaHist.png', dpi=300)
    
    print
    print fileName[:-4], ',', 
    for p in [p1, p2, p3, p4, p6, p5]:
        print p[0], ',', p[1], ',', p[2], ',',
    print
    
    # Save the data in the respective files
    fArea.write(fileName[:-4] + ', ')
    fArea.write( ', '.join( map(lambda mm: str(np.sqrt(mm)) , areaList)) + '\n')
    
    fNN.write(fileName[:-4] + ', ')
    fNN.write( ', '.join( map(lambda mm: str(mm) , nnDist)) + '\n')
    
    f.write(fileName[:-4] + ', ')
    for p in [p1, p2, p3, p4, p6, p5]:
        f.write('%f, %f, %f,' % (p[0], p[1], p[2]))
    f.write('\n')
            
    pl.show()
    pl.close('all')

    
f.close()    
fArea.close()    
fNN.close()    

print 'Total time taken : ', time.clock() - startTime