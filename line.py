import numpy as np
import matplotlib.pyplot as plt
import pylab

#========================= configurable parameters ======================================
# list of labels
labels = ['0kB', '512kB', '1024kB', '2048kB']
# number of data sets
n = len(labels)
# file format
# index data0 data1 data2 ...
# 1      3.1   2.2   1.3
# 2      5.2   3.7   4.4
# 3      4.2   1.5   9.6
# input file path
input_file = '/Users/yaowang/Desktop/results/stdout_none_detailed_astar_c0kB.trc'
# output file path
output_file = 
name_xaxis = "time (million cycles)"
name_yaxis = "# of cache misses"



#===================== DO NOT CHANGE BELOW THIS LINE ====================================
data = pylab.loadtxt(input_file)
counter = 0
for label in labels:
    counter++
    pylab.plot( data[:, 0], data[:, counter], label=cacheSize)
    
pylab.legend()
pylab.title(bench, fontsize=25)
pylab.xlabel(name_xaxis, fontsize=20)
pylab.ylabel(name_yaxis, fontsize=20)
plt.savefig(cpu + '_' + bench + '.pdf', bbox_inches='tight')
plt.close()
