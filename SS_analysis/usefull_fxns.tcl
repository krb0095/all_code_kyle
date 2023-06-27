# a lsit of tcl function for vmd that are super usefule 

proc get_ss {frame_num sel_string} {
	# frame_num == the current frame number 
	# sel == string to use for the selection 
	# all residues letter which are helical 
	set lookup {H G I}
	# go to the right frame 
	animate goto $frame_num
	set sel [atomselect top $sel_string]
	# recalc the ss 
	mol ssrecalc top 
	# get ss 
	set SS [$sel get structure]
	# set couter for n helix
	set helix 0
	foreach letter $lookup {
        	set temp [expr {[llength [split $SS $letter]] - 1}]
	        incr helix $temp
	    }
	# find the number of iotem ins the SS
	set len [llength $SS]
	set frac [expr {double($helix) / double($len) }]


	return "$frame_num $SS $frac"
}
	
proc get_sasa {framenum sel} { 
	set target_sel [atomselect top $sel]
	set pro [atomselect top protein]
	molinfo top set frame $framenum
	set sasa [measure sasa 1.4 $pro -restrict $target_sel]
	return $sasa
}

