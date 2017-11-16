#!/bin/bash

# some command that will read in the input from file of file_ext

for ext in list_of_file_ext:
    do this stuff:
    // maybe write new script to run each time i.e. "echo"
    ls */$ext > some_list
    
    root -l
    .L make_spect_graph.C

    create g0, g1, ..., gn, where n is the number of files with file_ext
    
    find date of each file with file_ext and echo to legend
    
    g0->SetTitle('file_ext')
    gn->Draw(kSomeColor+x) where x increased by 1 for each file with file_ext
    // will make a gradient
    
    make it so that it goes to the next file_ext after saving plot
