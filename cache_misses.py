import numpy as np
import matplotlib.pyplot as plt
import pylab

benchmarks = ['astar', 'bzip2', 'gcc', 'gobmk', 'h264ref', 'hmmer', 'libquantum', 'mcf', 'sjeng', 'xalan']
cpus = ['detailed', 'timing']
cacheSizes = ['0kB', '512kB', '1024kB', '2048kB']
folder = "/Users/yaowang/Desktop/results/"

for bench in benchmarks:
    for cpu in cpus:
        for cacheSize in cacheSizes:
            input_file = folder + 'stdout_none_' + cpu + '_' + bench + '_c' + cacheSize + '.trc'
            data = pylab.loadtxt(input_file)
            pylab.plot( data[:, 0], data[:, 1], label=cacheSize)
        pylab.legend()
        pylab.title(bench)
        pylab.xlabel("time")
        pylab.ylabel("# of cache misses")
        plt.savefig(cpu + '_' + bench + '.png', bbox_inches='tight')
        plt.close()