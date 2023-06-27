set psf [lindex $argv 0]
set dcd [lindex $argv 1]
set res_start [lindex $argv 2]
set res_end [lindex $argv 3]
set name [lindex $argv 4]
# load file 
mol load psf $psf 
mol addfile $dcd waitfor all 0
set OUT [open ./${name}_sasa_${res_start}-${res_end}.out w]
# find n frame 
set nframes [molinfo top get numframes]
# function to get the SS out 
source /media/bak11/KylesStuff/BPR-photo/analsysis/usefull_fxns.tcl
# loop into all frame 
puts $nframes
set sel "protein and resid $res_start to $res_end"
for {set i 0} {$i < $nframes} {incr i} {
#	puts $i
	# save the output of get_ss
	set ans [get_sasa $i $sel]
	puts $OUT $ans
}
# close the file 
close $OUT
exit
