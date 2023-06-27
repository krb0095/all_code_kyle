
set psf [lindex $argv 0]
set dcd [lindex $argv 1]
# select 1st residue
set res_start [lindex $argv 2] 
# selcet last resid 
set res_end [lindex $argv 3]
# name of the file 
set name [lindex $argv 4]
# load file 
mol load psf $psf 
mol addfile $dcd waitfor all 0
set OUT [open ./${name}_SS_for_${res_start}-${res_end}.out w]
# find n frame 
set nframes [molinfo top get numframes]
set lookup {H G I}
# function to get the SS out 
source /media/bak11/KylesStuff/BPR-photo/analsysis/usefull_fxns.tcl
# loop into all frame 
puts $nframes
set sel "protein and name CA and resid $res_start to $res_end"
for {set i 0} {$i < $nframes} {incr i} {
#	puts $i
	# save the output of get_ss
	set ans [get_ss $i $sel]
	puts $OUT $ans
}
# close the file 
close $OUT
exit
