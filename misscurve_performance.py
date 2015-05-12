#!/usr/bin/python

import sys
import numpy as np
import tsg_plot
import matplotlib.pyplot as plt
import pylab

specint = ['astar', 'bzip2', 'gcc', 'gobmk', 'h264ref', 'hmmer', 'libquantum', 'mcf', 'sjeng', 'xalan']
specinput = ['bzip2_chicken', 'bzip2_combined', 'bzip2_html', 'bzip2_liberty', 'bzip2_program', 'bzip2_test']
cpus = ['detailed']

folder = sys.argv[1]

benchmarks = specint
sim_ticks1 = 0
sim_insts1 = 0
sim_ticks2 = 0
sim_insts2 = 0
sim_ticks3 = 0
sim_insts3 = 0
sim_ticks4 = 0
sim_insts4 = 0
sim_insts_single1 = 0
sim_ticks_single1 = 0
sim_insts_single2 = 0
sim_ticks_single2 = 0
 
data = []

for bench1 in benchmarks:
    data_temp = []
    for bench2 in benchmarks:
        for cpu in cpus:
            flag1 = 0
            input_file = folder + 'static_' + cpu + '_' + bench1 + '_' + bench2 + '_c1024kB_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks1 = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts1 = int(line.split()[1])
                    if sim_insts1 > 2000000000:
                        flag1 = 1
                    break
            flag2 = 0
            input_file = folder + 'c_dynamic_' + cpu + '_' + bench1 + '_' + bench2 + '_c1024kB_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks2 = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts2 = int(line.split()[1])
                    if sim_insts2 > 2000000000:
                        flag2 = 1
                    break
            flag3 = 0
            input_file = folder + 'static_' + cpu + '_' + bench2 + '_' + bench1 + '_c1024kB_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks3 = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts3 = int(line.split()[1])
                    if sim_insts3 > 2000000000:
                        flag3 = 1
                    break
            flag4 = 0
            input_file = folder + 'c_dynamic_' + cpu + '_' + bench2 + '_' + bench1 + '_c1024kB_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks4 = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts4 = int(line.split()[1])
                    if sim_insts4 > 2000000000:
                        flag4 = 1
                    break
            # IPC for single application
            input_file = folder + 'none_' + cpu + '_' + bench1 + '_c1024kB_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks_single1 = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts_single1 = int(line.split()[1])
                    break
            input_file = folder + 'none_' + cpu + '_' + bench2 + '_c1024kB_stats.txt'
            inputfile = open(input_file, "r")
            for line in inputfile:
                searchResult = line.find("sim_ticks ")
                if searchResult != -1:
                    sim_ticks_single2 = int(line.split()[1])
                searchResult = line.find("sim_insts ")
                if searchResult != -1:
                    sim_insts_single2 = int(line.split()[1])
                    break
                    
            if flag1 == 0 or flag2 == 0:
                data_temp.append(0)
            else:
                IPC_static1 = 2000000000 * 500.0 / sim_ticks1
                IPC_dynamic1 = 2000000000 * 500.0 / sim_ticks2
                IPC_static2 = (sim_insts1 - 2000000000) * 500.0 / sim_ticks1
                IPC_dynamic2 = (sim_insts2 - 2000000000) * 500.0 / sim_ticks2
                IPC_single1 = sim_insts_single1 * 500.0 / sim_ticks_single1
                IPC_single2 = sim_insts_single2 * 500.0 / sim_ticks_single2
                WS_static = IPC_static1/IPC_single1 + IPC_static2/IPC_single2
                WS_dynamic = IPC_dynamic1/IPC_single1 + IPC_dynamic2/IPC_single2
                print bench1
                print bench2
                print WS_static
                print WS_dynamic
                speedup = WS_dynamic / WS_static
                data_temp.append(speedup)
    data.append(data_temp)

opts = tsg_plot.PlotOptions()
attribute_dict = \
{'bar_width': 0.7,
 # shreesha: I found this website to be nice for color schemes:
 # http://colorbrewer2.org/
 # 'colors': ['#ffffcc', '#78c679', '#006837'],
 'data': data,
 'fig': None,
 'figsize': (8, 2.5),
 'file_name': 'speedups.pdf',
 'fontsize': 8,
 'labels': [specint,specint],
 'labels_fontsize': 8,
 'legend_bbox': (0.0, 0.95, 1.0, 0.1),
 'legend_ncol': 5,
 'normalize_line': 1,
 'num_cols': 1,
 'num_rows': 1,
 'paper_mode': True,
 'plot_idx': 1,
 'rotate_labels': True,
 'rotate_labels_angle': -45,
 'scatter_bar': False,
 'scatter_bar_arrow': False,
 'scatter_bar_arrow_minlen': 0.2,
 'show': False,
 'stacked': False,
 'symbols': ['o', 'd', '^', 's', 'p', '*', 'x'],
 'title': 'Speedups',
 'xlabel': '',
 'ylabel': 'Speedup Normalized to Static Partitioning',
 'yrange': (0, 1.5)}
for name, value in attribute_dict.iteritems():
  setattr( opts, name, value )
tsg_plot.add_plot( opts )                
