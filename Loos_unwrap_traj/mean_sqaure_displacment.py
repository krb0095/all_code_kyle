import loos 
import loos.pyloos  
import numpy as np 
import argparse

def calculated_msd(trajectory):
    # obtain the msd 
    displacements = trajectory[1:] - trajectory[:-1]
    # sqaured displacmetns 
    squared_displacements = np.square(displacements)
    # calc MSD
    msd = np.mean(np.sum(squared_displacements, axis=1))
    return msd

def calculated_msd_lagged(trajectory,lag=1):
    # obtain the msd 
    displacements = trajectory[lag:] - trajectory[:-lag]
    # sqaured displacmetns 
    squared_displacements = np.square(displacements)
    # calc MSD
    msd = np.mean(np.sum(squared_displacements, axis=1))
    return msd

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
    parser.add_argument('--lag_range',
                        type=str,
                        default=False,
                        help='range of lag values to look into using the format start_lag:stride:end_lag'
    )
  
    args = parser.parse_args()
    system = loos.createSystem(args.system_file)
    traj = loos.pyloos.Trajectory(args.traj_file,
                                  system,
                                  stride=args.stride,
                                  skip=args.skip)
    lipid_sel =  loos.selectAtoms(system, args.selection_string)
    lipids =lipid_sel.splitByMolecule()
    num_lipids = len(lipids)
    num_frames= len(traj)
    # using the einstin stokes to get mean squared displacmnet 
    # to try reduce the memory using nump memmap 
    # find the szie of the array 
    output_size = (num_frames,num_lipids*3)
    mmap_type = np.float64
    # out array 
    filename = 'temp-msd-matrix.dat'
    # create the memmory map array 
    memmapped_array = np.memmap(filename,dtype=mmap_type, mode='w+',shape=output_size)
    # loop into the frame 
    cnt = 0
    for frame,i in zip(traj,range(output_size[0])):
        # loop into each frame
        lipid_coords =  np.array([[lip.centerOfMass()[0],lip.centerOfMass()[1],lip.centerOfMass()[2]] for lip in lipids])
        memmapped_array[i,:]= lipid_coords.flatten()

    # reformatinng the output array to the correct size 
    memmapped_array = memmapped_array.reshape(output_size[0],output_size[1]//3,3) # 3d array each box is one frame 
    # each row is one lipids and each column is a x y z postion 
    #print(calculated_msd(memmapped_array))  
    # create a list of lags 
    lags = np.arange(1,num_frames,1)
    if args.lag_range:
        start, stride , end = [int(i) for i in args.lag_range.split(':')]
        lags= np.arange(start,end,stride)
    print("# lag MSD")
    for lag in lags:
        print(lag,calculated_msd_lagged(memmapped_array,lag=lag))
