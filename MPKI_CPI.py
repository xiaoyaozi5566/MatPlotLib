#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

specint = ['astar', 'bzip2', 'gcc', 'gobmk', 'h264ref', 'hmmer', 'libquantum', 'mcf', 'sjeng', 'xalan']
specfp = ['dealII', 'lbm', 'milc', 'namd', 'povray', 'soplex', 'sphinx3']
specinput = ['bzip2_chicken', 'bzip2_combined', 'bzip2_html', 'bzip2_liberty', 'bzip2_program', 'bzip2_test']
cpus = ['timing', 'detailed']
cacheSizes = ['1kB', '128kB', '256kB', '384kB', '512kB', '640kB', '768kB', '896kB', '1024kB', '1152kB', '1280kB',
'1408kB', '1536kB', '1664kB', '1792kB', '1920kB', '2048kB']
# cacheSizes = ['1kB', '64kB', '128kB', '192kB', '256kB', '320kB', '384kB', '448kB', '512kB', '576kB', '640kB', '704kB',
# '768kB', '832kB', '896kB', '960kB', '1024kB']
cacheSizes = ['1', '128', '256', '384', '512', '640', '768', '896', '1024', '1152', '1280',
'1408', '1536', '1664', '1792', '1920', '2048']

folder = sys.argv[1]

benchmarks = specint
sim_ticks = 0
sim_insts = 0
l3_misses = 0

for bench in benchmarks:
    for cpu in cpus:
        f = open(cpu + "_" + bench +".curve", 'w')
        num_ways = 0
        MPKI = []
        CPI = []
        MPT = []
        for cacheSize in cacheSizes:
            flag = 0
            input_file = folder + cpu + '_' + bench + '_' + cacheSize + '_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts = int(line.split()[1])
                if cacheSize == '0kB':
                    searchResult = line.find("system.l2.overall_misses::total ")
                else:
                    searchResult = line.find("system.l2.overall_misses::total ")
                if searchResult != -1:
                    l2_misses = int(line.split()[1])
                    flag = 1
                    break
                else:
                    if line.find("End Simulation Statistics") != -1:
                        l2_misses = 0
                        flag = 1
                        break
                        
            if flag == 1:
                MPKI.append([num_ways, l2_misses*1000.0/sim_insts])
                CPI.append([num_ways, sim_ticks/500.0/sim_insts])
                MPT.append(l2_misses*500000000.0/sim_ticks)
            else:
                MPT.append(0)
            num_ways += 1
        
        print bench + " "
        # print CPI[7][1]/CPI[len(CPI)-1][1]
        for i in range(1, len(MPT)-1):
            if MPT[i] == 0:
                MPT[i] = (MPT[i-1] + MPT[i+1])/2
        for item in MPT:
            f.write("%s " % item)
        f.close()
        
        pylab.plot( np.array(MPKI)[:, 0], np.array(MPKI)[:, 1], label='')
        pylab.legend()
        pylab.title(bench, fontsize=25)
        pylab.xlabel("# of cache ways", fontsize=20)
        pylab.ylabel("MPKI", fontsize=20)
        plt.savefig(cpu + '_' + bench + '_MPKI.pdf', bbox_inches='tight')
        plt.close()
        
        pylab.plot( np.array(CPI)[:, 0], np.array(CPI)[:, 1], label='')
        pylab.legend()
        pylab.title(bench, fontsize=25)
        pylab.xlabel("# of cache ways", fontsize=20)
        pylab.ylabel("CPI", fontsize=20)
        plt.savefig(cpu + '_' + bench + '_CPI.pdf', bbox_inches='tight')
        plt.close()