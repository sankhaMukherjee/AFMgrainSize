# AFMgrainSize: Finding the grain size from AFM images ...

## What is it?

This is a Python program which will give you grain sized from AFM measurements. The assumption is that you have a number of "mounds", each of which is called a "grain". 

### Main Features

1. Just drag-drop the tab-delimited files into the data folder and you are good to go. 
2. You may need to change the `fileIO.py` file slightly simply because the way in which different AFMs convert data are slightly different. 
3. Example AFM files are provided in the `data` folder. 
4. This file was originally designed for studying the grain size of HDD multilayers (specifically the high-pressure Ru layer), but may conscivable be used for other purposes. 

### Dependencies

 - [Python 2.7](https://www.python.org)

## License

BSD


## Documentaton

Just dump the AFM files in the `data` folder and run `mainFile.py` as shown below. If you see results like that shown below, you are good to go. You may need to adjust the `fileIO.py` file to suit your own needs, as each AFM converts images a little differently. 

```bash
Sankha-desktop:office user$ ls
data            fileIO.py       imageProcess.py mainFile.py     plotFigures.py  results
Sankha-desktop:office user$ python mainFile.py 
['L211 BA-MD.txt']
[Reading File] data/L211 BA-MD.txt Line scan : ["\Adaptive Minimal Scan Size: 10"]
Pass 0
Line scan : ["\Scan Size: 250 nm"]
Pass 0
Pass 1
Pass 2
Pass 3
Pass 4
All pass
Line scan : ["\Scan Size: 0 0 ~m"]
Pass 0
Pass 1
Pass 2
Line scan : ["\Scan Size: 0 0 ~m"]
Pass 0
Pass 1
Pass 2
Line scan : ["\Scan Size: 0 0 ~m"]
Pass 0
Pass 1
Pass 2
# ----> Match for scan line: ["\Scan Size: 250 nm"
]
Time to read the file:  0.089427
,[Finding peaks] Time to find local Minima:  0.256438
Reducing multiple-peak points
Time to delete selected points:  0.051219
,[Finding Voronoi patches] Time to calculate voronoi tessletation:  0.008954
Time to calculate get arealist, and ptsList:  0.932937
,[Finding the heights] Time to do statistics:  7.526554
,[Calculating area statistics]

L211 BA-MD , 63.472102928 , 62.2326666717 , 13.0997622931 , 73.1701615839 , 3.66488973479 , 0.424038313095 , 83.5705827098 , 0.0561144418439 , 0.00954957831118 , 48.9955513065 , 6.01565755452 , 0.967429220116 , 60.9364459194 , 7.91652720839 , 0.827451517015 , 78.2233824716 , 6.5109858667 , 1.05303531086 ,
Total time taken :  10.900708
Sankha-desktop:office user$ 
```