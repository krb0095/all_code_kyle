#!/bin/bash

# this code is to run area per lipid 
# for simulations that have a protien in them 
# command line varaibles for the code 
system=$1 # stucuture file 
traj=$2 # trajectory file 
skip=$3 # number of frames to skip 
zmin=$4 # zpostion min 
zmax=$5 # zposition max
paddin=$6 #extra atoms to add to the calcuation for vorino to work 
proteinAndBilayer=$7 # selection for the protein and the bilayer
lipidOnly=$8 # selection for only the lipid 
halfNumber=$9 #number of lipids in half of the bilayer 
# run the run_areas code 
run_areas $system $traj $skip $zmin $zmax $paddin $proteinAndBilayer $lipidOnly > /tmp/lipid_areas.dat
# grab the header of the run_areas put them in the terminal
grep "#" /tmp/lipid_areas.dat 
# find the area pers lipid by dividing the area by the number of lipid per leaf
grep -v "#" /tmp/lipid_areas.dat | awk -v num=$halfNumber '{print $1 ,$2/$num,$3/$num}'
