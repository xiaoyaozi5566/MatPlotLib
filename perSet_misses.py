#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

specint = ['astar', 'bzip2', 'gcc', 'gobmk', 'h264ref', 'hmmer', 'libquantum', 'mcf', 'sjeng', 'xalan']
openssl = ['Blowfish', 'CAST5', 'RC4', 'SHA-0', 'SHA-1', 'SHA-256-224', 'SHA-512-384', 'Whirlpool']
cpus = ['detailed', 'timing']
cacheSize = '1024kB'

select_bench = sys.argv[1]
folder = sys.argv[2]

if select_bench == 'specint':
    benchmarks = specint
else:
    benchmarks = openssl

for bench in benchmarks:
    for cpu in cpus:
        input_file = folder + 'run_none_' + cpu + '_' + bench + '_c' + cacheSize + '_perSet_misses.trc'
        data = zip(*pylab.loadtxt(input_file))
        length = len(data[0])
        ratio = length/1024.0
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel("time (million cycles)", fontsize = 20)
        ax.set_ylabel("cache set", fontsize = 20)
        ax.set_title(bench + " cache misses over time", fontsize = 20)
        cax = ax.matshow(data, interpolation='nearest', aspect = ratio)
        fig.colorbar(cax)
        plt.savefig(cpu + '_' + bench + '_perSet.pdf', bbox_inches='tight')
        plt.close()
