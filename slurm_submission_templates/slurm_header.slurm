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




