### Kyle Billings Ph.D student at WVU mertz lab 
This github repository is a collection of all the code I have used over my career. I will try to keep this page updated as much as I can, and feel free to reach out if you so choose. The README.md give a brief break down of the codes, files, and directories here. I am in the process of ensuring all of the python codes are PIP3 format and that all other codes are as clear as possible but this will take some time. 
### List of files in the base directory 
| Filename      | content of file |
|:----------------------------------:|:---------------------------------------:|
|README.md                           | file for explaining the repository      |
|git-ssh-cheat-sheet.txt             | lines of code used to set up this github|
|list-of-useful-bash-commands.txt    | an ever growing list of useful bash code|


[//]: <> (This is a comment in markdown; below is a colasped list)

### Brake down of each folder and the materials inside

<details>
  <summary> common_analysis </summary>

  This folder contains code that should be run on almost every analyis for a trajecotry

  **Contains**
  - Vecotr_qunaites.py
    - This python code is useful for measuring the vector angle between two definded vectors. This code is written to use the libray LOOS to loop over the trajecory given and find the angle between the two user defined vectors . The code takes up tp  6 total commmand line arugmetns byut only 5 are required. We give the program the psf, dcd, name of atom 1 to set that point , name of atom 2 to draw the vecor of the given slection. The selection languge follows the loos syntax and can be more than one atom.
    - there is four use case for this program :
      - the 5th argument is 'x' telling the program to use the x axis for the vector angle
      - the 5th argument is 'y' telling the program to use the y axis for the vector angle
      - the 5th argument is 'z' telling the program to use the z axis for the vector angle
      - the 5th argument is the name of another atom of interset and is follwed by another atom to draw the vector to create a new vector 
  - dcc.py
    - This python code uses LOOS to load in a trjecotry with structual information and reutrns the dynamic cross correaltion matrix (DCC). This is an indication of correalted movent between residue pairs. (see the explation of DDC for more detial on the theory). The code takes the psf , the slection of tom to prefrom the DCC calcuations on , and any number of trajectory files. The output in a NXN matrix where N is the number of resides with the correaltion of residue pair montion.
      
**Explannation of DCC**

DCC is based of the standard pearson correation matrix of the selected atoms for analysis (typlically the C&#x0251; atoms). The following equation is used to compute the DCC.

$$DCC(i,j) = \dfrac{\langle \Delta r_{i}(t) \Delta r_{j}(t) \rangle}{\sqrt{\lVert \langle \Delta r_{i}(t) \rVert \rangle^{2}}\sqrt{\lVert \langle \Delta r_{j}(t) \rVert \rangle^{2}}}$$

Here delta R is defined as change in the postion of the atom at time t from the mean postion of that atom over the trajecotry.

$$\Delta r_{i/j} = r_{i/j}(t) - \langle r_{i/j}(t) \rangle $$

</details>

<details>
<summary> stat_find_production </summary>
<br>
  A directory containing code to help in the indentifaction of when production of MD simulations starts.
 
  **Contains**
 
  - simple_eq_check.py
    - Python code that when given a text file with measurnets will calculate the autocorrelation of the timeseries, returns the estimated frame at to strat analysis. This is done by using takeing a block of the data, finding the standard devation(stdev) of that block, and comparing that stdev to the wanted confidence interval. If that block is not less than the confidence interval another block of data is added untill we are less than the interval.
  - check_if_stationary.py
    - python code using Augmented Dickey-Fuller test to verifiy that the data is  stationary (aka at equalbrium) this is a work in progress, beacuse there is some memory isseus depending on the size of the data.


</details>

<details>
  <summary> Missing_loop_tool </summary>

  This folder contains the pyton code and an example bash scirpt for modeling missing loops into a protein chain
  
  **Contains**

  - genrated_seq_file.py
    - A python code that takes a user defined PDB file, the chain to work on, and the name of a outfile, and uses the modeller package to create a homology model of the missing loops.
  - do_all.sh
    - A bash scirpt example written to loop through a list of PDB files stored locally on the computer, and model in the missing loops
</details>


<details>
  <summary> SS_analysis </summary>

  This folder contains codes for find the SASA and secondary struccture analysis

  **Contains**

  - frame_sasa.tcl
    - A TCL code ran in VMD to find the solvent-accessible surface area over time of a given range of protein reisude. The code takes command line arguments for the psf, dcd, 1st residue, last resiude, and the prefix of the outfile. The code sources the path to useful function tcl code so the path will have to altered to adjust to your needs.
  - frame_ss.tcl
    - A TCL code made to run vmd to find the Secondary strucutre (SS) of residues perframe of the trajecotry. This is done over a user redifned range of residue indexs. This takes the psf, dcd, 1st residue, last reisude and preix of the run. Returns the frame index each resdiues SS and the precent helicity of that selection at a given frame.  The code sources the path to useful function tcl code so the path will have to altered to adjust to your needs.
  - usefull_fxns.tcl
    - A TCL set of functions to find the SS and SASA of one frame of a given slection in VMD. Must be soruced into the tcl code used in VMD for analysis.

</details>

<details>
  <summary> NAMD_ENERGY_VMD </summary>

  This folder containt the VMD tcl files to run namd energy in vmd

  **Contains**
  - target_to_target_namdE.tcl
    - This tcl code is to be used within VMD to execute namdEnergy. In the commandline it takes the arugemts of psf, dcd, selection 1, selection 2, and name of the file to output. There is one path that is hard coded into the code this time which is the path to the toppar files need to read in the stucture to namd. the solvent radius is set to 1.4 &#x212B; (standard for water as the solvent), the charmm36 cutoff distance (12 &#x212B;), and the charmm36 switch distacne (10 &#x212B;). Feel free to alter these vaules to suit your case
  - template_namd.namd
    - namd configeration filewith the basic infromation filled out.
</details>












    
