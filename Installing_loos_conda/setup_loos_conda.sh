#!/bin/bash 
# Kyle Billings 
# 6/28/23

# check if a program is 

# assume we can use conda 
conda activate 
# create loos env 
conda  create --name loos
# activate the env 
conda activate loos
conda install -c conda-forge loos
# check if we did install loos right 
interdist
