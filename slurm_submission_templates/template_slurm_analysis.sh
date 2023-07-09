#!/bin/bash
#SBATCH --job-name=NAME
#SBATCH --mail-user=krb0073@mix.wvu.edu
#SBATCH --nodes=NNODE
#SBATCH --ntasks=NTASK
#SBATCH --cpus-per-task=NCPU
#SBATCH -p QUE
#SBATCH --output=.%x_%A.out 

# change to where the job was submitted 
cd $SLURM_SUBMIT_DIR

# load loos 
module load loos/latest 
module load mertz_conda/latest
# just load the conda just in case 




# this file is to be catted to the end of the submission script to 
# run the functions we want 
# loos and conda are already good to go 
#  make teh out put dir 
data=/scratch/krb0073/BPR_SYS_ANALYSIS/Data # path to store the data 
output_name=OUT # place holder for the name of the data 

# loaction of all the traj 
loc=/scratch/krb0073/BPR_SYS_ANALYSIS/system_traj/

# now we list all of the dir in the traj 
systems=$(ls -d $loc*) # will work for anyone 

echo $systems

# loop into the folders given here 
for folder in $systems ; do
	
	# check if the item is a dir 
	if [[ -d $folder ]] ; then # if it is a folder contiune with what we are doing 

		# in this folder is my traj files 
		#### NOTE: for anyone reading this who all of this stuff is speacil to MY files 
		#### change to fit your needs please
		

		# in the foler there are my psf and traj links 
		# not all of the folders have the smae amount of traj 
		# save the nubmer of files name*.psf 
		total=$(ls $folder/*.psf |wc -l)
		
		# usign index 1 to $total loop over the traj 
		for index in $(seq 1 $total) ; do 
		
			# call the function that we want to run
			# inorder to make sure we are doing everything the way we want to 
			# this line must be hand edited 
			# note that we are going to place this a sbatch so we call the srun 
			
			# srun template 
			srun srun --exclusive --ntasks NT -c NCPUS [command to run here] & 
			
	fi 
done 

# wait for all the srun stuff to finish 
wait 

