
import numpy as np
import sys 
from scipy.constants import k 
"""This codes is used to find the KA (comperssion constant) of a bilayer"""
def find_ka_avarge(data,T=310.0):
    """Given a numpy 1d np array of area per lipids return the KA constant
    
    ------------------------------------------------------
    KA equation has the following from 
    KA = Kb*T <A> / <dA2>
    kb - boltzmann constant 
    T  - tempature K
   <A> - average Area per lipid 
  <da2>- mean sqaured fluxuations of the area

  returns the KA constat is J/[area unit]
    """
    # Find the mean sqaured flux of the area is respect to the average
    a_avg = data.mean()
    # mean squared flux from average
    flux = data - a_avg
    # find the mean sqaure flux 
    ms_flux = flux.mean()
    # find the comperssabaily constant
    ka = (k * T * a_avg)/ms_flux
    return ka , flux

def find_ka_frame_number(data,fnumber=0,T=310.0):
    """Given a numpy 1d np array of area per lipids return the KA constant
    
    ------------------------------------------------------
    KA equation has the following from 
    KA = Kb*T <A> / <dA2>
    kb - boltzmann constant 
    T  - tempature K
   <A> - average Area per lipid 
  <da2>- mean sqaured fluxuations of the area to the refrance frame

  returns the KA constat is J/[area unit]
    """

    # avgerage area 
    a_avg = data.mean()
    # msa to the given fnumber 
    flux = data - data[fnumber] # number must be <= lenght of the data -1
    # avg flux 
    ms_flux = flux.mean()
    ka = (k * T * a_avg)/ms_flux
    return ka , flux

if __name__ == "__main__":
 # command line arg for the file name 
 fname = sys.argv[1]
 # command line column number in python index  
 colnum = int(sys.argv[2])
 # temp in kelivn 
 T = float(sys.argv[3])
 # load in the area per lipid column 
 areas = np.loadtxt(fname=fname)[:,colnum] # will be 1D
 if len(sys.argv) == 5:
    # save as frame number and run using that refeance frame 
    frame_number = int(sys.argv[4])
    # the frame is assumed to be python index
    ka,fluxs = find_ka_frame_number(areas,fnumber=frame_number,T=T)
 else:
    # return ka and fluxs
    ka,fluxs = find_ka_avarge(areas,T=T)

 # print out call a line for the KA , the frame number , area_flux 
 print("#",*sys.argv) # all the command line items 
 print("# Average KA vaule",ka)
 # loop and print the flux vaules from the refracne
 fnum = 0
 for flux in fluxs:
    print(fnum,flux)
    fnum += 1 
