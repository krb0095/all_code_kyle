#!/bin/bash 

# kyle Billings 
# 7/7/23

# this code is to use the stride standalone package 
# we must have loos installed for this to work and
# i am going to assume that the user aleady has it on 
# also assumes the dcd is already processed

# command line args 
psf=$1
dcd=$2
sel=$3
path_to_stride=$4
prefix_name=$5
out_name=$6
# run dcdinfo to obtain the number of frames
nframes=$(dcdinfo $dcd | head -n 1 | awk '{print $7}')
# one less than nframes is the final index 
last_index=$(( nframes -1))
# print out the header realquick 
echo "#" "$(date)" > $out_name
echo "#" "$(basename $0)" $@ >> $out_name


# loop into each index
for frame in $(seq 0 $last_index); do 
	# step 1 create a temp pdb 
	frame2pdb -s "$sel" $psf $dcd $frame > /tmp/tmep_${prefix_name}.pdb
	# step 2 run stride 
	# grab the SS part we want at the end | sed -n '/[pattern]/,$p'
	# remove the the header| grep -v [pattern] 
	# grab the singel letter column | awk '{print $[colnum]}'
	# replace newline with space tr
	output=$($path_to_stride /tmp/tmep_${prefix_name}.pdb | sed -n '/|--Structure--|/,$p'| grep -v "|--Structure--|" | awk '{print $6}' | tr '\n' ' ' )
	# step 3 count total resiues in that pdb 
	total=$(echo $output | tr ' ' '\n' | wc -l)
	# step 4 count the number of helical residues 
	helix=$(echo $output | tr ' ' '\n' | grep -v T | grep -v C |grep -v E |grep -v B |grep -v b |wc -l)
	# step 5 find % helix 
	p_helix=$( echo "($helix / $total ) * 100" | bc -l)
	# step 6 print the SS string and the %helix 
	echo $output $p_helix 
	# step 7 rm teh temp file 
	rm /tmp/tmep_${prefix_name}.pdb
done >> $out_name
