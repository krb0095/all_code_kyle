### Kyle Billings Ph.D student at WVU mertz lab 
This github repository is a collection of all the code I have used over my career. I will try to keep this page updated as much as I can, and feel free to reach out if you so choose. The README.md give a brief break down of the codes, files, and directories here. I am in the process of ensuring all of the python codes are PIP3 format and that all other codes are as clear as possible but this will take some time. 
#### list of files in the base directory 
| Filename      | content of file |
|:----------------------------------:|:---------------------------------------:|
|README.md                           | file for explaining the repository      |
|git-ssh-cheat-sheet.txt             | lines of code used to set up this github|
|list-of-useful-bash-commands.txt    | an ever growing list of useful bash code|


[//]: <> (This is a comment in markdown; below is a colasped list)
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
