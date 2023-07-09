#!/bin/bash

# its silly but to stop me from over writing my template 
# ill call this code to create a new submssion script 

# command line arge for new name 
temp_name=$1 
# just cat the tempalte for the job we want 
sed "s/NAME/${temp_name}/g" template_analysis.slurm > ${temp_name}_analysis.slurm
# chmode to make a ex mostly for colors 
chmod u+x ${temp_name}_analysis.slurm

