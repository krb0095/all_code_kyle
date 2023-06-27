import loos
import loos.pyloos
import sys
from math import pi
import numpy as np
# system arguments
psf=sys.argv[1]

dcd=sys.argv[2]
# the selection should be one atom that is

atom1=sys.argv[3]
atom2=sys.argv[4]

atom3 = sys.argv[5]
# check what atom 3 is
normal = True
if atom3 == 'x':
    norm = loos.GCoord(1 , 0 , 0)
elif atom3 == 'y':
    norm = loos.GCoord(0 , 1 , 0)
elif atom3 == 'z':
    norm = loos.GCoord(0 , 0 , 1)
else:
    normal = False
    atom4 =sys.argv[6]

# the system must be orianted such that the bilayer plane is
# in the XY
system = loos.createSystem(psf)
# load the dcd
traj = loos.pyloos.Trajectory(dcd,system)
a1 = loos.selectAtoms(system,atom1)
a2 = loos.selectAtoms(system,atom2)
if not normal:
    a3 = loos.selectAtoms(system,atom3)
    a4 = loos.selectAtoms(system,atom4)

print("#frameNumber angle")
for frame in traj:
    # loop in to each frame of the traj
    # find the vector between atoms 1 and 2
    point1 = a1.centroid() # this is a loos GCoord item
    point2 = a2.centroid() # this too
    # case 1 want the bilayer normal
    # find the a2 - a1 unit vector
    vect1 = point2 -point1
    uv1 = vect1 / vect1.length()
    if normal:
        # with the unit vectors made convert to numpy for the rest
        # typically the dot product between the two is
        # equal to u dot v = |U||V| cos theta
        # for a unit vector the magnteiudes, | | are 1
        # u dot v = cos theta
        # but the arccos is not contious so a better form would be
        # theta = arhtan2(|u cross v| , u dot v )
        # jwwalker.com/pages/angle-between-vectors.html#:~:text=tan(θ)%3D∥u,v∥u∙v.
        dot_prod = loos.GCoord.dot(uv1,norm)
        cross_prod = loos.GCoord.cross(uv1,norm).length()
        # find the archtan in rads
        dot_prod = np.array([dot_prod])
        cross_prod = np.array([cross_prod])
        theta = np.arctan2(cross_prod,dot_prod)
        # convert to degrees
        #  rad = (theta * 180) / pi
        theta  = (theta * 180 ) / pi
    else:
        # this case has another user defined vector
        point3 = a3.centroid()
        point4 = a4.centroid()
        # convert to a unit vector
        vect2 = point4 - point3
        uv2 = vect2/vect2.length()
        # same a bove just not using the x , y , or z axis
        dot_prod = loos.GCoord.dot(uv1,uv2)
        cross_prod = loos.GCoord.cross(uv1,uv2).length()
        dot_prod = np.array([dot_prod])
        cross_prod = np.array([cross_prod])
        # find the archtan in rads
        theta = np.arctan2(cross_prod,dot_prod)
        # convert to degrees
        #  rad = (theta * 180) / pi
        theta  = (theta * 180 ) / pi
    # print the frame and the angel out to the terminal
    print(traj.index(),theta[0])
