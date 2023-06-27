# command line psf
set psf [lindex $argv 0]
# command line dcd
set dcd [lindex $argv 1]
# command line selection 1
set sel1 [lindex $argv 2]
# cmd line selection 2
set sel2 [lindex $argv 3]
# name of the file to give out
set outfile [lindex $argv 4]
# there are different cutoff for different md setups
# we are using the charmm 36 cut off to find
set cutoff 12
set switchdist 10
# load in psf and dcd file to vmd
mol load psf $psf
mol addfile $dcd waitfor all 0
# path to the toppar folder
set common /media/bak11/
#atom selection for each sel
set A [atomselect 0 "$sel1"]
set B [atomselect 0 "$sel2"]



# all we want is the pair interaction energy of the selections
# from the lariat peptide namd E
# require namdenergy
package require namdenergy
# get all the energies between the two selection
# update sel is slow but if we want to get
# energhies for something that within a distance is needed
# have to add in all of the parameter file
namdenergy -ofile $outfile -sel $A  $B -all -vdw namd2 \
-par "$common/toppar/par_all36_cgenff.prm" \
-par "$common/toppar/par_all36m_prot.prm" \
-par "$common/toppar/par_all36_na.prm" \
-par "$common/toppar/par_all36_carb.prm" \
-par "$common/toppar/par_all36_lipid.prm" \
-par "$common/toppar/toppar_water_ions_namd.str"\
-par "$common/toppar/retinal-pro.str"\
-par "$common/toppar/retinal-dpro.str"



exit
exit
