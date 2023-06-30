#!/usr/bin/env python

"""
Unwraps a systems perdoic box of for each frame of a
given selection. This creates an output for calcuting the
means sqaured diffusion.
"""

"""
  This file is part of LOOS.
  LOOS (Lightweight Object-Oriented Structure library)
  Copyright (c) 2021 Alan Grossfield, Grossfield Lab
  Department of Biochemistry and Biophysics
  School of Medicine & Dentistry, University of Rochester
  This package (LOOS) is free software: you can redistribute it and/or modi>  it under the terms of the GNU General Public License as published by
  the Free Software Foundation under version 3 of the License.
  This package is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import loos
import loos.pyloos
import numpy as np
import argparse
def fullhelp():
    print("""lipid_unwrap.py takes the coordinates from a trajectory file to unwrap
    the periodic box for a selection. At the moment the only rectangular
    box based periodic box conditions are able to be used. The subset of atoms
    that you use could be any valid loos selection, but the program is intended
    to work on lipids,tracking the geometric center of a molecule at the
    current frame and comparing that position to the previous one.
    If the difference between the two positions vary by more than half of the
    periodic box length (in x,y, or z) a correction factor is added to the
    current position to correct the positions it moves outside the boundaries.

    If desired, a pdb and DCD of the unwrapped trajectory can be. This is done by
    taking every molecule if the selection to (0,0,0) then translating it to the
    unwrapped. For making the trajectory, the assumption is made that the
    Lx, Ly or Lz of the periodic box will not be greater than 1000000 Angstroms.

    The output text file containing the radial position of the atom comparing
    it to the center of mass to the bilayer.

    Usage: lipid_unwrap.py [OPTIONS] selection_string system_file trajectory_file
        --  selection_string identifies the atoms to be analyzed. They will be
            split by molecule number calculate position for every lipid adjusted
            without the wrapping
        --  system_file is a PDB, PSF, prmtop, etc
        --  trajectory_file eg DCD, xtc. Its contents must precisely
            match the system file

    Options:
        --skip: # of residues to exclude from the front of each trajectory
        --stride: how to step through the trajectory (eg --stride 10 will read
              every 10th frame)
        --fullhelp: prints this message
        --output_traj: output a dcd of the unwrapped trajectory default(--output_traj 0)
        --output_prefix: prefix to use for the output default is output

    Example:
    python3 lipid_unwrap.py --ouput_traj 1 --output_prefix='unwrapped_foo' foo.psf 'resname == "POPC"' foo.dcd

    We will obtain a dcd of the unwrapped trajectory with the name of
    unwrapped_foo.dcd a pdb of unwrapped_foo.pdb to be used to view the dcd, and
    unwrapped_foo.txt that has the radial distantness of the center of the lipid
    to the COM of bilayer at that frame for the POPC lipids in the membrane
    """)

# This code is based of the paper https://arxiv.org/pdf/2111.12052.pdf
# they have a robust mwthod of unwrappingthe trajecotry in NTP
# using equaiton 12 
# xui+1 = xiu + (xwi+1 + xwi)-
# floor((xiw+1 -xwi1/Li+11)+1/2)*Li+1 -
# floot((xiw+1 -xwi1/Li+11))*(Li+1 -Li)
# xui+1 = unwrapped postions of the atoms time +1
# xui = unwrapped postion at time t 
# xwi+1 = wrapped postion at time t+1
# xw = wrapped postion at time t
# Li+1 = PBC deminasions 

# functions to return new unwrapped postions
def heuristic_method(xu,xi1,li1):
    xui1 = 0 
    xui1 += xi1
    delta = xi1 - xu
    delta /= li1 
    delta += 1/2
    delta = np.floor(delta)
    delta *= li1
    xui1 -= delta 
    return xui1
def displacement_method(xu,xi,xi1,li1):
    xui1 = 0
    xui1 += xu 
    xui1 += (xi1 - xi)
    delta = xi1 - xi
    delta /= li1 
    delta += 1/2
    delta = np.floor(delta)
    delta *= li1
    xui1 = np.subtract(xui1,delta) 
    return xui1
def ntp_method(xu,xi,xi1,li,li1):
    xui1 = 0
    xui1 += xu 
    xui1 += (xi1 -xi)
    # floor term 1
    delta = (xi1 - xi )
    delta /= li1
    delta += 1/2
    delta = np.floor(delta)
    delta *= li1
    # subtract the floor tern to xui1
    xui1 = np.subtract(xui1,delta) 
    # second floor term 
    delta = xi - xu 
    delta /= li 
    delta += 1/2
    delta = np.floor(delta)
    delta *= (li1-li)
    xui1 = np.subtract(xui1,delta) 
    return xui1 

class FullHelp(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        kwargs['nargs'] = 0
        super(FullHelp, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        fullhelp()
        parser.print_help()
        setattr(namespace, self.dest, True)
        parser.exit()

if __name__ in '__main__':
    parser = argparse.ArgumentParser(description="Unwrap PBC lipids")
    parser.add_argument('system_file',
                        help="File describing the system")
    parser.add_argument('selection_string',
                        help="Selection string describing which residues to use")
    parser.add_argument('traj_file',
                        help="File contraing the trajecotry")
    parser.add_argument('--fullhelp',
                        help="Print detailed description of all options",
                        action=FullHelp)
    parser.add_argument('--skip',
                        type=int,
                        default=0,
                        help='# of frame to skip')
    parser.add_argument('--stride',
                        type=int,
                        default=1,
                        help="Read every nth frame")
    parser.add_argument('--output_traj',
                        type=int,
                        default=0,
                        help='produce an unwrapped trajectory')
    parser.add_argument('--output_prefix',
                        default='unwrapped_output',
                        type=str,
                        help='name of the tractory file to write (DCD format)')
    parser.add_argument('--no_center',
                        default=1,
                        type=int,
                        help='Do not wrap the trajecotry default is to center the lipid selection')
    args = parser.parse_args()
    pre = args.output_prefix
    system = loos.createSystem(args.system_file)
    traj = loos.pyloos.Trajectory(args.traj_file,
                                  system,
                                  stride=args.stride,
                                  skip=args.skip)

        # select the atoms for the lipids
    # split into the individual molecules of lipid
    lipid_sel =  loos.selectAtoms(system, args.selection_string)
    lipids =lipid_sel.splitByMolecule()
    num_lipids = len(lipids)
    num_frames= len(traj)

    pre = args.output_prefix



    all_centers = np.zeros((num_frames,num_lipids*3))

    
    if args.output_traj:
        outtraj = loos.DCDWriter(pre + ".dcd")
    # this is the order of the lipid resname-resid-segname
    for frame in traj:
        # obtain pbc 
        #frame.centerAtOrigin()
        pbc = frame.periodicBox()
        # set a blank loos atomic group 
        output =  loos.AtomicGroup()
        if traj.index() == 0:
            # we have no need to update the unwrapped postions 
            xi = lipid_sel.getCoords()
            # xu is the same as xi 
            xu = np.copy(xi)
            li = np.array([i for i in pbc])
            if args.output_traj:
                output.periodicBox(loos.GCoord(1000000, 1000000, 1000000))
                frame_copy = lipid_sel.copy()
                
                for lipid in frame_copy:
                    output.append(lipid)
                pdb = loos.PDB.fromAtomicGroup(output)
                with open(f'{pre}.pdb','w') as out_pdb:
                    out_pdb.write(str(pdb))
                outtraj.writeFrame(output)
                



        else: 
            # define the parts
            # xu and xi defiend already 
            # deifne the new xiu1 
            xi1 = lipid_sel.getCoords()
            # find x_ui1 
            li1 = np.array([i for i in pbc])
            #xui1 = ntp_method(xu,xi,xi1,li,li1)
            xui1 = heuristic_method(xu,xi1,li1)
            #xui1 = displacement_method(xu,xi,xi1,li1)
            
            # CODE For loos to make a pdb traj 
            if args.output_traj:
                output.periodicBox(loos.GCoord(1000000, 1000000, 1000000))
                frame_copy = lipid_sel.copy()
                # shift the frame copy 
                shifted= frame_copy.setCoords(xui1)
                #pdb = loos.PDB.fromAtomicGroup(shifted)
                for lipid in frame_copy:
                    output.append(lipid)
                outtraj.writeFrame(output)

            # update xi and l1 
            xi = np.copy(xi1)
            li = np.copy(li)
            xu = np.copy(xui1)
           
            