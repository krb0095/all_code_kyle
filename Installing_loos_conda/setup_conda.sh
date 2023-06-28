#!/bin/bash 
# Kyle Billings

# This code is used in linux to automatically configure loos to work 

# function to check if a package is installed or not 
# assumes we do not have sudo so we exit is there is no packge 

isPackageInstalled () {
	# given the name of the wanted pacakge exit the code if the"
	#Package is not there"
	# use dpkg to check if the item is there 
	# dpkg --status <packagename> puts out the status of the package
	# if a packge is not there then we get nothing 
	# the pacakge is not there we can't run the code and exit
	# all messages send the out put to /dev/null
	if  ! (dpkg --status $1 &> /dev/null) ; then
		# this means that we do not have the packge
		# tell the user that we do not have the package 
		echo "$1 is not installed please try agian after installing $1"
		# exit a code 
		exit 
	fi 
}

isPackageNotInstalled () {
        # given the name of the wanted pacakge exit the code if the"
        #Package is not there"
        # use dpkg to check if the item is there
        # dpkg --status <packagename> puts out the status of the package
        # if a packge is not there then we get nothing
        # the pacakge is not there we can't run the code and exit
        # all messages send the out put to /dev/null
        if   (dpkg --status $1 &> /dev/null) ; then
                # this means that we do not have the packge
                # tell the user that we do not have the package
                echo "$1 is installed there is no reason to run this code to install $1"
                # exit a code
                exit
	else 
		# print we are going to install the code 
		echo "$1 is not installed so we will continue the code"
        fi
}

# test for wget 
isPackageInstalled wget 
# test for conda 
isPackageNotInstalled conda
# if we are still running the code then we get the sh for miniconda 
wget -c "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"  -O "Miniconda3.sh"
# run the sh code 
bash Miniconda3.sh # follow the prompts 
source ~/.bashrc  # soruce the bashrc to have conda work 
# we are now in a conda env 
# fixing the automatic conda entracne
conda config --set auto_activate_base false
# exit conda beaacue we are done
#conda deactivate 


