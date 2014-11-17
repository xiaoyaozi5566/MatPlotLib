#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
    
specint = ['astar', 'bzip2', 'gcc', 'gobmk', 'h264ref', 'hmmer', 'libquantum', 'mcf', 'sjeng', 'xalan']
openssl = ['Blowfish', 'CAST5', 'RC4', 'SHA-0', 'SHA-1', 'SHA-256-224', 'SHA-512-384', 'Whirlpool']
cpus = ['detailed', 'timing']
cacheSizes = ['0kB', '512kB', '1024kB', '2048kB']

select_bench = sys.argv[1]
folder = sys.argv[2]

if select_bench == 'specint':
    benchmarks = specint
else:
    benchmarks = openssl

for bench in benchmarks:
    for cpu in cpus:
        for cacheSize in cacheSizes:
            input_file = folder + 'run_none_' + cpu + '_' + bench + '_c' + cacheSize + '.trc'
            data = pylab.loadtxt(input_file)
            pylab.plot( data[:, 0], movingaverage(data[:, 1], 10), label=cacheSize)
        pylab.legend()
        pylab.title(bench, fontsize=25)
        pylab.xlabel("time (million cycles)", fontsize=20)
        pylab.ylabel("# of cache misses", fontsize=20)
        plt.savefig(cpu + '_' + bench + '.pdf', bbox_inches='tight')
        plt.close()
