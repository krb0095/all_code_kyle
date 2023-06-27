# kyle billings
# 2/23/22
import loos
import loos.pyloos
import numpy as np
import sys
# system arguments
psf=sys.argv[1]

sel=sys.argv[2] # takes multiple traj
dcd=sys.argv[3:]

# looad the stcuture information
system = loos.createSystem(psf)

#make a list of traj
trajs =  [loos.pyloos.Trajectory(d,system,subset=sel) for d in dcd]

# make the allgind version
traj = loos.pyloos.AlignedVirtualTrajectory(trajs[0],alignwith=sel)
for t in trajs:
    traj.append(t)


# average stucuture for equalbrium postion
avg = loos.pyloos.averageStructure(traj).getCoords()
# natoms
n = len(loos.selectAtoms(system,sel))
# split the slection given by
subset = loos.selectAtoms(system,sel).splitByMolecule()

# split into x y z matrices
# getting all of the coords from the traj
coords = loos.pyloos.extractCoords(traj)
# reshape the ocrds to be frames X [x1,y1,z1,x2...]
coords = (np.array(coords).T)

# slice the coords inot x ,y ,z compiomrys
xpos,ypos,zpos=coords[:,::3] ,coords[:,1::3] ,coords[:,2::3]

# makes a 3d matrix of xyz being one matrix
xyz = np.dstack((xpos,ypos,zpos)) # frames X atoms X number of axis
# per frame aka row


out = np.zeros((n,n)) # make the stoageb matirx
cnt = 0

for jth in range(xyz.shape[0]):
#        print(jth)
        # find the dispacment from the last frame
        # ith is the frame before jth is the frame after
        disp = xyz[jth,:] -avg
        # dot prodcut o the matrix to its self
        out += np.dot(disp,disp.T)
        cnt += 1
# normalize by number of frames
X = out/cnt
# normal lize
nn =np.zeros((n,n))
norm = np.diagonal(X)
row = 0
for i in norm:
    col = 0
    for j in norm:
        nn[row,col] = i**0.5 * j**0.5
        col +=1
    row+=1
for i in X/nn:
    print(*i)
