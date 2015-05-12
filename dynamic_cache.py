#!/usr/bin/python

import sys
import tsg_plot
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab

specint = ['astar', 'bzip2', 'gcc', 'gobmk', 'h264ref', 'hmmer', 'libquantum', 'mcf', 'sjeng', 'xalan', 'soplex']
cpus = ['detailed']
H_mins = ['1', '2', '4']
thresholds = ['2', '5', '10', '20']

multiprog = [['astar', 'bzip2'],
             ['bzip2', 'astar'],
             ['astar', 'mcf'],
             ['mcf', 'astar'],
             ['libquantum', 'h264ref'],
             ['h264ref', 'libquantum'],
             ['libquantum', 'xalan'],
             ['xalan', 'libquantum'],
             ['astar', 'gobmk'],
             ['gobmk', 'astar'],
             ['libquantum', 'hmmer'],
             ['hmmer', 'libquantum'],
             ['gcc', 'bzip2'],
             ['h264ref', 'gobmk'],
             ['gobmk', 'h264ref'],
             ['mcf', 'hmmer'],
             ['hmmer', 'mcf'],
             ['xalan', 'sjeng'],
             ['sjeng', 'xalan'],
            ]

multiprog = [['mcf', 'bzip2'],
             ['xalan', 'soplex'],
             ['bzip2', 'xalan'],
             ['soplex', 'mcf'],
             ['bzip2', 'mcf'],
             ['soplex', 'xalan'],
             ['xalan', 'bzip2'],
             ['mcf', 'soplex'],
             
             ['mcf', 'astar'],
             ['xalan', 'astar'],
             ['soplex', 'libquantum'],
             ['bzip2', 'libquantum'],
             ['astar', 'mcf'],
             ['astar', 'xalan'],
             ['libquantum', 'soplex'],
             ['libquantum', 'bzip2'],
                          
             ['bzip2', 'h264ref'],
             ['h264ref', 'bzip2'],
             ['mcf', 'gobmk'],
             ['hmmer', 'mcf'],
             ['xalan', 'sjeng'],
             ['hmmer', 'xalan'],
             ['soplex', 'h264ref'],
             ['gobmk', 'soplex'],
             
             ['astar', 'libquantum'],
             ['sjeng', 'gobmk'],
             ['hmmer', 'sjeng'],
             ['astar', 'h264ref'],
            ]
            
folder = sys.argv[1]

# single_IPC = {'soplex'  : 0.35574262786}
single_IPC = {}

# get the IPC for single benchmark
for bench in specint:
    input_file = folder + bench + '_stats.txt'
    inputfile = open(input_file, "r")
    sim_ticks = 0
    sim_insts = 0
    start_tick = 0
    end_tick = 0
    counter = 0
    for line in inputfile:
        searchResult = line.find("sim_ticks ")
        if searchResult != -1:
            counter += 1
            if counter == 2:
                sim_ticks = int(line.split()[1])
                break
        searchResult = line.find("sim_insts ")
        if searchResult != -1:
            sim_insts = int(line.split()[1])
        # if sim_insts < 1100000000 and sim_insts >= 1000000000:
#             start_tick = sim_ticks
#         if sim_insts < 2100000000 and sim_insts >= 2000000000:
#             end_tick = sim_ticks
#             break;
    # single_IPC[bench] = 250000000.0*500/(end_tick - start_tick)
    single_IPC[bench] = 250000000.0*500/sim_ticks

print single_IPC

static_speedup = []

for workload in multiprog:
    p0 = workload[0]
    p1 = workload[1]
    input_file = folder + 'stdout_detailed_static_' + p0 + '_' + p1 + '.out'
    inputfile = open(input_file, "r")
    flag = 0
    pattern = 0
    for line in inputfile:
        searchResult = line.find("REAL SIMULATION")
        if searchResult != -1:
            flag = 1
        if flag == 1:
            searchResult = line.find("reached the max instruction count")
            if searchResult != -1:
                searchResult = line.find("cpu1")
                if searchResult != -1:
                    pattern = 1
                break
    inputfile.close()                
    
    input_file = folder + 'detailed_static_' + p0 + '_' + p1 + '_stats.txt'
    inputfile = open(input_file, "r")
    counter = 0
    sim_ticks0 = 0
    sim_ticks1 = 0
    for line in inputfile:
        searchResult = line.find("sim_ticks ")
        if searchResult != -1:
            counter += 1
            if counter == 3:
                if pattern == 0:
                    sim_ticks0 = int(line.split()[1])
                else:
                    sim_ticks1 = int(line.split()[1])
            elif counter == 4:
                if pattern == 0:
                    sim_ticks1 = int(line.split()[1])
                else:
                    sim_ticks0 = int(line.split()[1])
                break;
    
    if sim_ticks0 == 0:
        IPC0 = 0
    else:
        IPC0 = 250000000.0*500/sim_ticks0
    if sim_ticks1 == 0:
        IPC1 = 0
    else:
        IPC1 = 250000000.0*500/sim_ticks1
        
    if IPC0 == 0 or IPC1 == 0:
        weighted_speedup = 0
    else:
        # weighted_speedup = 2/(single_IPC[p0]/IPC0 + single_IPC[p1]/IPC1)
        weighted_speedup = IPC0/single_IPC[p0] + IPC1/single_IPC[p1]
    static_speedup.append(weighted_speedup)

dynamic_speedup = []
dynamic_speedup_each = []

for workload in multiprog:
    p0 = workload[0]
    p1 = workload[1]
    max_speedup = 0
    exception = 0
    for H_min in H_mins:
        if exception == 1:
            break
        for threshold in thresholds:
            input_file = folder + 'stdout_detailed_dynamic_' + p0 + '_' + p1 + '_' + H_min + '_' + threshold + '.out'
            inputfile = open(input_file, "r")
            flag = 0
            pattern = 0
            for line in inputfile:
                searchResult = line.find("REAL SIMULATION")
                if searchResult != -1:
                    flag = 1
                if flag == 1:
                    searchResult = line.find("reached the max instruction count")
                    if searchResult != -1:
                        searchResult = line.find("cpu1")
                        if searchResult != -1:
                            pattern = 1
                        break
            inputfile.close()
            
            input_file = folder + 'detailed_dynamic_' + p0 + '_' + p1 + '_' + H_min + '_' + threshold + '_stats.txt'
            inputfile = open(input_file, "r")
            counter = 0
            sim_ticks0 = 0
            sim_ticks1 = 0
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    counter += 1
                    if counter == 3:
                        if pattern == 0:
                            sim_ticks0 = int(line.split()[1])
                        else:
                            sim_ticks1 = int(line.split()[1])
                    elif counter == 4:
                        if pattern == 0:
                            sim_ticks1 = int(line.split()[1])
                        else:
                            sim_ticks0 = int(line.split()[1])
                        break;
    
            if sim_ticks0 == 0:
                IPC0 = 0
            else:
                IPC0 = 250000000.0*500/sim_ticks0
            if sim_ticks1 == 0:
                IPC1 = 0
            else:
                IPC1 = 250000000.0*500/sim_ticks1       
            if IPC0 == 0 or IPC1 == 0:
                weighted_speedup = 0
            else:
                # weighted_speedup = 2/(single_IPC[p0]/IPC0 + single_IPC[p1]/IPC1)
                weighted_speedup = IPC0/single_IPC[p0] + IPC1/single_IPC[p1]
            # if weighted_speedup == 0:
            #     max_speedup = 0
            #     exception = 1
            #     break
            dynamic_speedup_each.append(weighted_speedup)
            if weighted_speedup > max_speedup:
                max_speedup = weighted_speedup
    
    dynamic_speedup.append(max_speedup)

utility_speedup = []

for workload in multiprog:
    p0 = workload[0]
    p1 = workload[1]
    input_file = folder + 'stdout_detailed_utility_' + p0 + '_' + p1 + '.out'
    inputfile = open(input_file, "r")
    flag = 0
    pattern = 0
    for line in inputfile:
        searchResult = line.find("REAL SIMULATION")
        if searchResult != -1:
            flag = 1
        if flag == 1:
            searchResult = line.find("reached the max instruction count")
            if searchResult != -1:
                searchResult = line.find("cpu1")
                if searchResult != -1:
                    pattern = 1
                break
    inputfile.close()                
    
    input_file = folder + 'detailed_utility_' + p0 + '_' + p1 + '_stats.txt'
    inputfile = open(input_file, "r")
    counter = 0
    sim_ticks0 = 0
    sim_ticks1 = 0
    for line in inputfile:
        searchResult = line.find("sim_ticks ")
        if searchResult != -1:
            counter += 1
            if counter == 3:
                if pattern == 0:
                    sim_ticks0 = int(line.split()[1])
                else:
                    sim_ticks1 = int(line.split()[1])
            elif counter == 4:
                if pattern == 0:
                    sim_ticks1 = int(line.split()[1])
                else:
                    sim_ticks0 = int(line.split()[1])
                break;
    
    if sim_ticks0 == 0:
        IPC0 = 0
    else:
        IPC0 = 250000000.0*500/sim_ticks0
    if sim_ticks1 == 0:
        IPC1 = 0
    else:
        IPC1 = 250000000.0*500/sim_ticks1
        
    if IPC0 == 0 or IPC1 == 0:
        weighted_speedup = 0
    else:
        # weighted_speedup = 2/(single_IPC[p0]/IPC0 + single_IPC[p1]/IPC1)
        weighted_speedup = IPC0/single_IPC[p0] + IPC1/single_IPC[p1]
    utility_speedup.append(weighted_speedup)

nopar_speedup = []

for workload in multiprog:
    p0 = workload[0]
    p1 = workload[1]
    input_file = folder + 'stdout_detailed_nopar_' + p0 + '_' + p1 + '.out'
    inputfile = open(input_file, "r")
    flag = 0
    pattern = 0
    for line in inputfile:
        searchResult = line.find("REAL SIMULATION")
        if searchResult != -1:
            flag = 1
        if flag == 1:
            searchResult = line.find("reached the max instruction count")
            if searchResult != -1:
                searchResult = line.find("cpu1")
                if searchResult != -1:
                    pattern = 1
                break
    inputfile.close()                
    
    input_file = folder + 'detailed_nopar_' + p0 + '_' + p1 + '_stats.txt'
    inputfile = open(input_file, "r")
    counter = 0
    sim_ticks0 = 0
    sim_ticks1 = 0
    for line in inputfile:
        searchResult = line.find("sim_ticks ")
        if searchResult != -1:
            counter += 1
            if counter == 3:
                if pattern == 0:
                    sim_ticks0 = int(line.split()[1])
                else:
                    sim_ticks1 = int(line.split()[1])
            elif counter == 4:
                if pattern == 0:
                    sim_ticks1 = int(line.split()[1])
                else:
                    sim_ticks0 = int(line.split()[1])
                break;
    
    if sim_ticks0 == 0:
        IPC0 = 0
    else:
        IPC0 = 250000000.0*500/sim_ticks0
    if sim_ticks1 == 0:
        IPC1 = 0
    else:
        IPC1 = 250000000.0*500/sim_ticks1
        
    if IPC0 == 0 or IPC1 == 0:
        weighted_speedup = 0
    else:
        # weighted_speedup = 2/(single_IPC[p0]/IPC0 + single_IPC[p1]/IPC1)
        weighted_speedup = IPC0/single_IPC[p0] + IPC1/single_IPC[p1]
    nopar_speedup.append(weighted_speedup)
    
cat = []
data = []
subcat = ['static', 'dynamic', 'utility']

for workload in multiprog:
    cat.append(workload[0]+'_'+workload[1])

for i in range(len(static_speedup)):
    data.append([nopar_speedup[i], static_speedup[i], dynamic_speedup[i], utility_speedup[i]])

# Set up plotting options
opts = tsg_plot.PlotOptions()
opts.data = data
opts.labels = [cat, subcat]

attribute_dict = \
    {
        'show' : False,
        'file_name' : 'partitioning.pdf',
        'paper_mode' : True,
        'figsize' : (6, 3),
        'xlabel' : 'Workload',
        'ylabel' : 'Weighted Speedup',
        'yrange' : (1, 2.5),
        'legend_ncol' : 3,
        'rotate_labels' : True,
        'rotate_labels_angle' : -45
    }
for name, value in attribute_dict.iteritems():
  setattr( opts, name, value )

# Plot
tsg_plot.add_plot( opts )

count = 0
for H_min in H_mins:
    for threshold in thresholds:
        data = []
        for i in range(len(static_speedup)):
            data.append([nopar_speedup[i], static_speedup[i], dynamic_speedup_each[i*12+count], utility_speedup[i]])
        # Set up plotting options
        opts = tsg_plot.PlotOptions()
        opts.data = data
        opts.labels = [cat, subcat]

        attribute_dict = \
            {
                'show' : False,
                'file_name' : 'partitioning_'+ H_min + '_' + threshold + '.pdf',
                'paper_mode' : True,
                'figsize' : (6, 3),
                'xlabel' : 'Workload',
                'ylabel' : 'Weighted Speedup',
                'yrange' : (1, 2.5),
                'legend_ncol' : 3,
                'rotate_labels' : True,
                'rotate_labels_angle' : -45
            }
        for name, value in attribute_dict.iteritems():
          setattr( opts, name, value )

        # Plot
        tsg_plot.add_plot( opts )
        count += 1
    
    
        